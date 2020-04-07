# -*- coding: utf-8 -*-
# Filename: reporter by: andrek
# Timesamp:2018-11-04 :: 23:46 using PyCharm

import json
import collections
import sys
import os
import traceback
import time

from src import config, di, sys_path, reporters_path
from src.utils.helpers import singleton
from  src.utils.three2two import iteritems


logger = di.get("Logger")


class Reporter(object):
	class QueueReader:
		def __init__(self, q, block=False, timeout=None):
			"""
			 :param Queue.Queue q:
			 :param bool block:
			 :param timeout:
			"""
			self.q = q
			self.block = block
			self.timeout = timeout

		def __enter__(self):
			return self.q.get(self.block, self.timeout)

		def __exit__(self, _type, _value, _traceback):
			self.q.task_done()

	def __init__(self): # Might use call here
		di.get("Logger").debug("Loading available reports")
		self.header = 'report_'
		self.load_reports()
		self.queue = di.get("Queue")

	def send_data(self, report_data, reporters=None, *args, **kwargs):
		ok = True
		if reporters is None:
			return self._reporters[config.defaults.reporter].send_data(report_data, *args, **kwargs)
		else:
			try:
				for reporter in reporters:
					ok = ok and self._reporters[reporter].send_data(report_data, *args, **kwargs)
				return ok
			except KeyError as ke:
				logger.error("Error: {}".format(ke))
				logger.error(traceback.format_exc())
				return False

	def load_reports(self, *args):
		"""Wrapper to load: metrics and export modules."""
		#sys.path.insert(0,reporters_path)
		# Init the metrics dict
		self._reporters = collections.defaultdict(dict)

		# Load the reporters
		"""Load all metrics in the 'metrics' folder."""
		update = []
		for item in os.listdir(reporters_path):
			if not item.startswith('_') and not item.endswith('.pyc') and "__pycache__" not in item:
				update.append(self._load_report(os.path.basename(item),
												args=args))
				print("hoj {0}").format(os.path.basename(item))


		# Init the export modules dict
		# self._exports = collections.defaultdict(dict)

		# Load the export modules
		# self.load_exports(args=args)

		# Restoring system path
		sys.path = sys_path

	def _load_report(self, report, config=None, *args, **kwargs):
		"""Load the reporter, init it and add to the _reporters dict"""
		# The key is the reporter name
		# for example, the file reporter_xxx.py
		# generate self._reporter["xxx"] = ...
		name_full = report[len(self.header):-3].lower()
		# This will break if the file name is messed up

		name = "%s%s" % (name_full[0].upper(), name_full[1:]) + "Reporter"

		try:
			# Import the metric
			print(report, name)
			report = __import__(report[:-3])
			# Init and add the metric to the dictionary
			cls = getattr(report, name)
			self._reporters[name] = cls(args=args, kwargs=kwargs)
			return self._reporters[name]

		except Exception as e:
			# If a metric can not be log, display a critical message
			# on the console but do not crash
			logger.error("Error while initializing the {} metric ({})".format(name, e))
			logger.error(traceback.format_exc())

	def queue_messages(self, q, block=False, timeout=None):
		"""
		 :param Queue.Queue q:
		 :param bool block:
		 :param int timeout:
		"""
		while not q.empty():
			with self.QueueReader(q, block, timeout) as row:
				yield row

	def process_queue(self):
		while True:
			time.sleep(0.5)
			for msg in self.queue_messages(di.get("Queue")):
				self.send_data(msg)


