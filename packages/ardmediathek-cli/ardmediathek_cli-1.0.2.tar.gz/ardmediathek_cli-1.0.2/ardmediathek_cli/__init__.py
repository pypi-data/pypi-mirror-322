#!/usr/bin/env python
#-*- coding:utf-8 -*-

import argparse
import datetime
import email.utils
import json
import logging
import os
import re
import sys
import time
from urllib.parse import urlparse

import coloredlogs
import enlighten
import miniupnpc
import prefixed
import requests
import requests_cache

import ardmediathek

download_queue = []
pbar_man = enlighten.get_manager()
__requests_cache_backend = requests_cache.backends.filesystem.FileCache("~/.cache/ardmediathek-cli/")

coloredlogs.install()
logging.addLevelName(35, "MESSAGE")

def get_ip_country():
	u = miniupnpc.UPnP()
	u.discoverdelay = 200
	u.discover()
	u.selectigd()
	ip = u.externalipaddress()
	url = "http://freegeoip.net/json/" + ip
	r = requests.get(url)
	js = r.json()
	print(js["country_code"])
	return js["country_code"]

def is_geoblocked_unavailable(broadcast):
	return broadcast.geoblocked and get_ip_country() not in ["DE", "AT", "CH"]

class DownloadJob:
	def __init__(self, broadcast):
		self.broadcast = broadcast
		self.program = ardmediathek.get_program(self.broadcast.program_id)
		self.broadcast.program = self.program
	
	def get_stream_size_bytes(self, args):
		stream_url = self.get_stream_url(args)
		if stream_url == None or is_geoblocked_unavailable(self.broadcast):
			return 0
		with requests_cache.session.CachedSession() as session:
			r = session.head(stream_url)
		content_length = int(r.headers["Content-Length"])
		if content_length < 1000000:
			logging.getLogger("ardcli").warn(
				f"Stream data size too small for {ardmediathek.get_broadcast_api_url(self.broadcast.id)}"
			)
			return 0
		return int(r.headers["Content-Length"])
	
	def get_output_path(self, args):
		# regexr.com/8aq93
		broadcast_title = re.sub(r"(?<=\(\d)\/(?=\d\))", " von ", self.broadcast.title)
		output_path = os.path.join(
			args.output,
			args.path_template.format(
				broadcast_title=broadcast_title,
				program_title=self.program.title,
				station_name=self.broadcast.station.name
			)
		)
		return output_path
	
	def get_stream_url(self, args):
		if len(self.broadcast.streams) == 0:
			logging.getLogger("ardcli").error(f"No streams found for {ardmediathek.get_broadcast_api_url(self.broadcast.id)}")
			return None
		quality = args.quality
		if not args.quality in map(lambda s: s.quality, self.broadcast.streams):
			quality = 3
		
		stream_url = list(filter(lambda s: s.quality == quality, self.broadcast.streams))[0].url
		return stream_url
	
	def download(self, args):
		if is_geoblocked_unavailable(self.broadcast):
			logging.getLogger("ardcli").error("Cannot download geoblocked broadcast from outside DE / AT / CH")
			return False
		stream_url = self.get_stream_url(args)
		if not stream_url:
			return False
		output_path = self.get_output_path(args)
		broadcast_json = self.broadcast.json()
		logging.getLogger("ardcli").info(f"Starting download to '{output_path}'")
		logging.getLogger("ardcli").debug(f"API URL: {ardmediathek.get_broadcast_api_url(self.broadcast.id)}")
		
		r = requests.get(stream_url, stream=True)
		
		content_length = float(r.headers["Content-Length"])
		if content_length < 1000000:
			logging.getLogger("ardcli").error(
				f"Stream data size too small for {ardmediathek.get_broadcast_api_url(self.broadcast.id)}"
			)
			return False
		last_modified = email.utils.parsedate_to_datetime(r.headers["Last-Modified"])
		mp4_time = datetime.datetime(1, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
		mp4_length = 0
		json_time = datetime.datetime(1, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
		json_length = 0
		if os.path.exists(output_path + ".mp4"):
			mp4_time = datetime.datetime.fromtimestamp(
				os.path.getmtime(output_path + ".mp4"),
				tz=datetime.timezone.utc
			)
			mp4_length = os.path.getsize(output_path + ".mp4")
		if os.path.exists(output_path + ".json"):
			json_time = datetime.datetime.fromtimestamp(
				os.path.getmtime(output_path + ".json"),
				tz=datetime.timezone.utc
			)
			json_length = os.path.getsize(output_path + ".json") 
		
		should_write_mp4 = False
		should_write_json = False
		if mp4_time < last_modified or mp4_length < content_length:
			should_write_mp4 = True
		if json_time < last_modified or json_length < len(broadcast_json):
			should_write_json = True
		
		pbar = pbar_man.counter(
			position=2,
			total=float(content_length),
			desc=f"Current download",
			unit="B",
			unit_scale=True,
			leave=False,
			bar_format="{desc}{desc_pad}{percentage:3.0f}%|{bar}| " \
				"{count:!.2h}{unit} / {total:!.2h}{unit} " \
				"[{elapsed} < {eta}, {rate:!.2h}{unit}/s]"
		)
		
		if should_write_json or should_write_mp4:
			os.makedirs(os.path.dirname(output_path), exist_ok=True)
		
		if should_write_mp4:
			with open(output_path + ".mp4", "wb") as f:
				for chunk in r.iter_content(args.block_size):
					f.write(chunk)
					pbar.update(float(len(chunk)))
		else:
			logging.getLogger("ardcli").info("Not downloading MP4 file - was already downloaded")
		if should_write_json:
			with open(output_path + ".json", "w") as f:
				f.write(json.dumps(self.broadcast.json()))
		else:
			logging.getLogger("ardcli").debug("Not writing JSON data file - already existing and complete")
		pbar.close(clear=True)
		
		return True

def add_broadcast_job(id, args):
	try:
		broadcast = ardmediathek.get_broadcast(id)
		logging.getLogger("ardcli").debug(f"Adding broadcast '{broadcast.title}' to job queue")
	except ardmediathek.exceptions.InvalidBroadcastIDException as e:
		logging.getLogger("ardcli").error(repr(e))
		return
	job = DownloadJob(broadcast)
	download_queue.append(job)

def add_program_job(id, args, pbar):
	try:
		program = ardmediathek.get_program(id)
		logging.getLogger("ardcli").debug(f"Adding program '{program.title}' to job queue")
	except ardmediathek.exceptions.InvalidProgramIDException as e:
		logging.getLogger("ardcli").error(repr(e))
		return
	broadcast_ids = program.get_broadcast_ids()[::-1]
	pbar.total += len(broadcast_ids)
	for broadcast_id in broadcast_ids:
		add_broadcast_job(broadcast_id, args)
		pbar.update()

def add_url_job(url, args, pbar):
	id = list(filter(None, url.split("/")))[-1]
	if "video" in url:
		add_broadcast_job(id, args)
	elif "sendung" in url:
		add_program_job(id, args)

def main():
	argp = argparse.ArgumentParser(description="CLI interface to the ardmediathek.de API")
	level_names = sorted(logging.getLevelNamesMapping().items(), key=lambda item: item[1])
	level_names = list(map(lambda item: item[0].lower(), level_names))
	argp.add_argument(
		"--log-level",
		help="Minimum log level for log messages to be printed",
		default="info",
		choices=level_names
	)
	
	subparsers = argp.add_subparsers(dest="command")
	subparsers.required = True
	
	argp_api_url = subparsers.add_parser("api-url", help="Print API URL for a given program or broadcast URL")
	argp_api_url.add_argument(
		"url",
		nargs=1,
		help="URL of the broadcast or program to print the API URL for"
	)
	
	argp_dl = subparsers.add_parser("dl", help="Download a broadcast or a program")
	argp_dl.add_argument(
		"-b", "--broadcast-id",
		help="ID of the broadcast to download",
		action="append"
	)
	argp_dl.add_argument(
		"-p", "--program-id",
		help="ID of the program to download",
		action="append"
	)
	argp_dl.add_argument(
		"url",
		help="URL(s) of the broadcast(s) or program(s) to download",
		nargs="*"
	)
	argp_dl.add_argument(
		"-q", "--quality",
		help="Preferred stream download quality (0=HVGA, 1=VGA, 2=DVGA, 3=HD, 4=FHD)",
		choices=[0, 1, 2, 3, 4],
		default=3,
		type=int
	)
	argp_dl.add_argument(
		"--block-size",
		help="Download block size",
		type=int,
		default=1000
	)
	argp_dl.add_argument(
		"--path-template",
		help="Output path template",
		default=os.path.join(
			"{station_name}",
			"{program_title}",
			"{broadcast_title} I {program_title} I {station_name}"
		)
	)
	argp_dl.add_argument(
		"-o", "--output",
		help="Output directory",
		default=os.path.join(os.path.expanduser("~"), "Videos")
	)
	
	args = argp.parse_args()
	args.log_level = args.log_level.upper()
	
	dummy = pbar_man.counter(total=100, leave=False)
	dummy.close(clear=True)
	
	logging.basicConfig(
		level="INFO",
		format="{asctime} {name} [{levelname}] {message}",
		datefmt="%H:%M:%S",
		style="{"
	)
	logger = logging.getLogger("ardcli")
	try:
		logging.getLogger().setLevel(args.log_level)
		logger.setLevel(args.log_level)
	except ValueError as e:
		logger.warn(f"Unknown log level: {args.log_level}, setting to INFO")
	logger.info(f"Log level: {logging.getLevelName(logger.level)}")
	
	if args.command == "api-url":
		type, id = ardmediathek.get_id_from_url(args.url[0])
		if type == "broadcast":
			print(ardmediathek.get_broadcast_api_url(id))
		else:
			print(ardmediathek.get_program_api_url(id))
			program = ardmediathek.get_program(id)
			for broadcast in program.get_broadcasts():
				print(ardmediathek.get_broadcast_api_url(broadcast.id))
	elif args.command == "dl":
		logger.info(f"Preferred download quality: {ardmediathek.get_quality_name(args.quality)}")
		logger.info(f"Downloading to {args.output}")
		logger.info(f"Path template: {args.path_template}")
		
		bc_ids = args.broadcast_id or []
		prog_ids = args.program_id or []
		for url in args.url:
			type, id = ardmediathek.get_id_from_url(url)
			if type == "broadcast":
				bc_ids.append(id)
			else:
				prog_ids.append(id)
		
		broadcast_pbar = pbar_man.counter(
			total=1,
			desc="Adding broadcasts",
			unit="",
			leave=False,
			bar_format="{desc}{desc_pad}{percentage:3.0f}%|{bar}| " \
				"{count:.0f} {unit} / {total:.0f} {unit} " \
				"[{elapsed} < {eta}, {rate:.0f} {unit}/s]"
		)
		broadcast_pbar.total = 0
		
		for broadcast_id in bc_ids:
			add_broadcast_job(broadcast_id, args)
			broadcast_pbar.update()
		
		if prog_ids:
			program_pbar = pbar_man.counter(
				total=len(prog_ids),
				desc="Adding programs",
				unit="",
				leave=False,
				bar_format="{desc}{desc_pad}{percentage:3.0f}%|{bar}| " \
					"{count:.0f} {unit} / {total:.0f} {unit} " \
					"[{elapsed} < {eta}, {rate:.0f} {unit}/s]"
			)
			program_pbar.refresh()
			for program_id in prog_ids:
				add_program_job(program_id, args, broadcast_pbar)
				program_pbar.update()
			
			program_pbar.close(clear=True)
		broadcast_pbar.close(clear=True)
		
		num_jobs = len(download_queue)
		logger.info(f"Number of download jobs: {num_jobs}")
		
		size_pbar = pbar_man.counter(
			total=len(download_queue),
			desc="Getting broadcast stream sizes",
			unit="",
			leave=False,
			bar_format="{desc}{desc_pad}{percentage:3.0f}%|{bar}| " \
				"{count:.0f} {unit} / {total:.0f} {unit} " \
				"[{elapsed} < {eta}, {rate:.0f} {unit}/s]"
		)
		total_bytes = prefixed.Float(0)
		for job in download_queue:
			total_bytes += job.get_stream_size_bytes(args)
			size_pbar.update()
		logger.info(f"Total data to download: {total_bytes:!.2H}")
		size_pbar.close(clear=True)
		
		dl_pbar = pbar_man.counter(
			total=len(download_queue),
			desc="Downloading broadcasts",
			unit="",
			bar_format="{desc}{desc_pad}{percentage:3.0f}%|{bar}| " \
				"{count:.0f} {unit} / {total:.0f} {unit} " \
				"[{elapsed} < {eta}, {rate:.0f} {unit}/s]"
		)
		dl_pbar_success = dl_pbar.add_subcounter(color="green")
		dl_pbar_fail = dl_pbar.add_subcounter(color="red")
		dl_sbar = pbar_man.status_bar(
			status_format="Downloading broadcast '{download_name}'",
			fields={"download_name": ""}
		)
		
		for job in download_queue:
			dl_sbar.update(download_name=os.path.split(job.get_output_path(args))[-1])
			dl_sbar.refresh()
			result = False
			while not result:
				try:
					result = job.download(args)
				except requests.exceptions.ChunkedEncodingError:
					logger.warn("Download failed with ChunkedEncodingError - retrying")
				else:
					break
				
			if result:
				dl_pbar_success.update()
			else:
				dl_pbar_fail.update()

