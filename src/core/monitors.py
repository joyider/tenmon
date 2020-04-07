# -*- coding: utf-8 -*-
# Filename: monitors.py by: andrek
# Timesamp:2017-10-03 :: 00:33 using PyCharm Community Edition

import collections
import os
import sys
import threading
import traceback

from src import di, metrics_path, exm_path, sys_path
from src import metrics_path as exports_path

from src.core.updater import Updater

logger = di.get("Logger")

available_job_classes = ['Monitors', 'Exm']

class BaseMonitor(object):

	"""This class stores, updates and gives stats."""
	# update = []


	def __init__(self, config=None, *args, **kwargs):
		# Set the config instance
		self.config = config

		# Set the argument instance
		self.args = args
		try:
			self.typ = kwargs['cls']
		except KeyError:
			pass
			logger.debug("Loading {} modules: ".format(self.typ))

		# Instance of Updater
		#Will contain all update methods for all monitors
		self.updates = None
		self.monupdates = []

		# Load metrics and exports modules
		self.load_modules(self.args)

		# Load the limits (for metrics)
		# self.load_confines(self.config)

	def __getattr__(self, item):
		"""Overwrite the getattr method in case of attribute is not found.
		The goal is to dynamically generate the following methods:
		- getmetricname(): return metricname stat in JSON format
		- getViewsmetricname(): return views of the metricname stat in JSON format
		"""
		# Check if the attribute starts with 'get'
		if item.startswith('getViews'):
			# Get the metric name
			metricname = item[len('getViews'):].lower()
			# Get the metric instance
			metric = self._metrics[metricname]
			if hasattr(metric, 'get_json_views'):
				# The method get_views exist, return it
				return getattr(metric, 'get_json_views')
			else:
				# The method get_views is not found for the metric
				raise AttributeError(item)
		elif item.startswith('get'):
			# Get the metric name
			metricname = item[len('get'):].lower()
			# Get the metric instance
			metric = self._metrics[metricname]
			if hasattr(metric, 'get_stats'):
				# The method get_stats exist, return it
				return getattr(metric, 'get_stats')
			else:
				# The method get_stats is not found for the metric
				raise AttributeError(item)
		else:
			# Default behavior
			raise AttributeError(item)

	def load_modules(self, args):
		"""Wrapper to load: metrics and export modules."""

		# Init the metrics dict
		self._metrics = collections.defaultdict(dict)

		# Load the metrics
		self.load_metrics(args=args)

		# Restoring system path
		sys.path = sys_path

	def _load_metric(self, metric, config=None, *args, **kwargs):
		"""Load the metric (script), init it and add to the _metric dict"""
		# The key is the metric name
		# for example, the file metrics_xxx.py
		# generate self._metrics_list["xxx"] = ...
		name_full = metric[len(self.header):-3].lower()
		# This will break if the file name is messed up

		name = "%s%s" % (name_full[0].upper(), name_full[1:])+self.classifier

		try:
			# Import the metric
			metric = __import__(metric[:-3])
			# Init and add the metric to the dictionary
			cls = getattr(metric, name)
			self._metrics[name] = cls(args=args, kwargs=kwargs)
			return self._metrics[name]

		except Exception as e:
			# If a metric can not be log, display a critical message
			# on the console but do not crash
			logger.error("Error while initializing the {} metric ({})".format(name, e))
			logger.error(traceback.format_exc())

	def load_metrics(self, args=None):
		"""Load all metrics in the 'metrics' folder."""

		for item in os.listdir(self.mon_path):
			if not item.startswith('_') and not item.endswith('.pyc') and "__pycache__" not in item:
				self.monupdates.append(self._load_metric(os.path.basename(item),
				                  args=args, config=self.config))


class Monitors(BaseMonitor):

	# Script header constant
	header = "metric_"
	mon_path = metrics_path
	classifier = "Update"

	def __init__(self, config=None, *args, **kwargs):
		kwargs['cls'] = self.__class__.__name__
		super(Monitors, self).__init__(config, *args, **kwargs)
		self.updates = Updater(*self.monupdates)

	def update(self):
		"""Wrapper method to update the metrics."""
		self.updates.update_now()

	def report(self):
		"""Wrapper for the check reporting"""
		self.updates.report_now()

	def getAllmetrics(self, enable=True):
		"""Return the enable metrics list.
		if enable is False, return the list of all the metrics"""
		if enable:
			return [p for p in self._metrics if self._metrics[p].is_enabled]
		else:
			return [p for p in self._metrics]

	def load_confines(self, config=None):
		"""Load the stats confines (except the one in the exclude list)."""
		# For each metrics, call the load_confines method
		for p in self._metrics:
			self._metrics[p].load_confines(config)


	def getAll(self):
		"""Return all the stats (list)."""
		return [self._metrics[p].get_raw() for p in self._metrics]

	def getAllAsDict(self):
		"""Return all the stats (dict)."""
		return {p: self._metrics[p].get_raw() for p in self._metrics}

	def getAllLimits(self):
		"""Return the metrics limits list."""
		return [self._metrics[p].limits for p in self._metrics]

	def getAllLimitsAsDict(self, metric_list=None):
		"""
		Return all the stats limits (dict).
		Default behavor is to export all the limits
		if metric_list is provided, only export limits of given metric (list)
		"""
		if metric_list is None:
			# All metrics should be exported
			metric_list = self._metrics
		return {p: self._metrics[p].limits for p in metric_list}

	def getAllViews(self):
		"""Return the metrics views."""
		return [self._metrics[p].get_views() for p in self._metrics]

	def getAllViewsAsDict(self):
		"""Return all the stats views (dict)."""
		return {p: self._metrics[p].get_views() for p in self._metrics}

	def get_metric_list(self):
		"""Return the metric list."""
		return self._metrics

	def get_metric(self, metric_name):
		"""Return the metric name."""
		if metric_name in self._metrics:
			return self._metrics[metric_name]
		else:
			return None

	def end(self):
		"""End of the Metric statistics."""
		# Close export modules
		for e in self._exports:
			self._exports[e].exit()
		# Close metrics
		for p in self._metrics:
			self._metrics[p].exit()


class Exm(BaseMonitor):
	# Script header constant
	header = "exm_"
	mon_path = exm_path
	classifier = "Exm"

	def __init__(self, config=None, *args, **kwargs):
		kwargs['cls'] = self.__class__.__name__
		super(Exm, self).__init__(config, *args, **kwargs)

	def execute(self):
		"""Wrapper method to update the metrics."""
		return self.monupdates
