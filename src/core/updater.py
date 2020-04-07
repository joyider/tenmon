# -*- coding: utf-8 -*-
#
# Filename: updateinterface by: andrek
# Timesamp:2018-10-31 :: 15:30 using PyCharm

import json
from abc import abstractmethod

import src.utils.three2two as three2two
from src import di
from src.core.reporter import Reporter

logger = di.get("Logger")


class Updater:
	"""
	Interface for our Monitor UPDATE behaviour
	"""

	def __init__(self, *args, **kwargs):
		"""

		:param args: Tuple of Monitor Updates to instanciate
		:param kwargs: Optional List of KeyWord args.
		"""
		self.monitor = {}
		self.metrics = []
		self.reports = []

		# self.reporter = reporter.Reporter()
		# Update behaviours as a tuple from the client
		if args:
			for monitor in args:
				self.monitor[monitor.__class__.__name__] = monitor

	def update_now(self, *args, **kwargs):
		"""
		Abstract class that needs to be implemented in all Monitors
		:param args: Optional list of Monitors to update
		:param kwargs: Optional list of KeyWord args
		:return: List of stats from all updated monitors
		"""

		self.metrics = []

		logger.info("Do something before real update")
		# IF no args then update all update behaviours in list
		if not args:
			for (classname, instance) in three2two.iteritems(self.monitor):
				# Return data from monitor (classname)
				stat = instance.update(*args, **kwargs)
				logger.info("Do something with THIS update metrics for monitor {}".format(classname))
				# This is now a list of dicts, probably not OK, need dict
				self.metrics.append(stat)

		# We have args and only update those behaviours
		else:
			for inst in args:
				cname = inst.__class__.__name__
				if cname in self.monitor:
					stat = inst.update(**kwargs)
					logger.info("Do something with THIS update metrics for monitor {}").format(cname)
					# This is now a list of dicts, probably not OK, need dict
					self.metrics.append(stat)

		# Do something with all update metrics

		# for metric in self.metrics:
		#	print(metric)
		return self.metrics

	def report_now(self, *args, **kwargs):
		"""
		Abstract class that needs to be implemented in all Monitors
		:param args: Optional list of Monitors to update
		:param kwargs: Optional list of KeyWord args
		:return: List of stats from all updated monitors
		"""

		self.reports = []

		logger.info("Do something before real update")
		# IF no args then update all update behaviours in list
		if not args:
			for (classname, instance) in three2two.iteritems(self.monitor):
				# Return data from monitor (classname)
				stat = instance.report(*args, **kwargs)
				logger.info("Do something with THIS update metrics for monitor {}".format(classname))
				# This is now a list of dicts, probably not OK, need dict
				self.reports.append(stat)

		# We have args and only update those behaviours
		else:
			for inst in args:
				cname = inst.__class__.__name__
				if cname in self.monitor:
					stat = inst.report(**kwargs)
					logger.info("Do something with THIS update metrics for monitor {}").format(cname)
					# This is now a list of dicts, probably not OK, need dict
					self.reports.append(stat)

		logger.info("Do something with all update metrics")

		for adict in self.reports:
			di.get("Reporter").send_data(adict)
		return self.reports

	@staticmethod
	def result_logger(fct):
		"""Log (DEBUG) the result of the function fct."""

		def wrapper(*args, **kw):
			ret = fct(*args, **kw)
			logger.debug("%s %s %s return %s" % (
				args[0].__class__.__name__,
				args[0].__class__.__module__[len('metric_'):],
				fct.__name__, ret))
			return ret

		return wrapper