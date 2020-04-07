# -*- coding: utf-8 -*-
#
# Filename: updateinterface by: andrek
# Timesamp:2018-10-31 :: 15:30 using PyCharm

import json
from abc import abstractmethod, ABCMeta

import src.utils.three2two as three2two
from src import di
import src.core.reporter as reporter

logger = di.get("Logger")


class UpdateInterface:
	__metaclass__ = ABCMeta
	"""
	Interface for our Monitor UPDATE behaviour
	"""
	def __init__(self, *args, **kwargs):
		metric_name = self.__class__.__module__[len('metric_'):]


	@abstractmethod
	def update(self, *args, **kwargs):
		"""
		Abstract class that needs to be implemented in all Monitors
		:param args: Optional list of Monitors to update
		:param kwargs: Optional list of KeyWord args
		:return: List of stats from all updated monitors
		"""
		pass



	@abstractmethod
	def report(self, *args, **kwargs):
		"""
		Abstract class that needs to be implemented in all Monitors
		:param args: Optional list of Monitors to update
		:param kwargs: Optional list of KeyWord args
		:return: List of stats from all updated monitors
		"""
		pass

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