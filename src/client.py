# -*- coding: utf-8 -*-
#
# Filename: client by: andrekarlsson
# Timesamp: 2018-11-05 :: 13:29

import sched
import time
import os

import src.utils.scheduler as scheduler

from src import config
from src import di
from src.core.monitors import Monitors, Exm


class Client:

	def __init__(self, *args, **kwargs):
		self._logger = di.get("Logger")
		self.check_time = int(config.checks.freq)
		self.report_time = int(config.reporting.freq)
		self.sched_checks = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)
		self.sched_reports = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)
		self.monitors = Monitors()

	def loop(self):
		"""
		This is a wrapper for __loop function,
		:return: Nothing
		"""

		scheduler.every(self.check_time).seconds.do(self.monitors.update)
		scheduler.every(self.report_time).seconds.do(self.monitors.report)

		while True:
			scheduler.run_pending()
			time.sleep(1)

	def end(self):
		"""
		End Resources
		:return: Nothing

		"""
		pass


class Exms:

	def __init__(self, *args, **kwargs):
		self._logger = di.get("Logger")
		self.exms = Exm()

	def loop(self):
		"""
		This is a wrapper for __loop function,
		:return: Nothing
		"""
		return self.exms.execute()


	def end(self):
		"""
		End Resources
		:return: Nothing

		"""
		pass


class Reporter:

	def __init__(self, *args, **kwargs):
		self._logger = di.get("Logger")
		self.reporter = di.get("Reporter")

	def loop(self):
		self.reporter.process_queue()


"""
if __name__ == "__main__":
	config.add_config_ini('./config.ini')
	di.get("Logger").info('Starting')
	print('%s %s' % (config.auth.jwt_token, config.auth.identifier))
	config.kalle.kula = 'test'
	print('%s %s %s' % (config.auth.jwt_token, config.auth.identifier, config.kalle.kula))
	Client().loop()
"""

