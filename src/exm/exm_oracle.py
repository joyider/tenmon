import os
import time
import json

from src.config import BaseConfig as CONF
from src import di


class OracleExm:
	def __init__(self, *args, **kwargs):
		self.logger = di.get("Logger")
		self.queue = di.get("Queue")
		print("OracleExm Inited")

	def __call__(self, *args, **kwargs):
		self.logger = di.get("Logger")
		self.queue = di.get("Queue")

	# TODO: Add file not exist exception
	def _follow(self, thefile):
		thefile.seek(0, 2)
		while True:
			line = thefile.readline()
			if not line:
				time.sleep(0.1)
				continue
			yield line

	def start(self):
		logfile = open("/tmp/alert_devmon.log", "r")
		loglines = self._follow(logfile)

		while True:
			for line in loglines:
				print(line)
				self.queue.put_nowait(line)

	def aprint(self):
		print(self.logger)
