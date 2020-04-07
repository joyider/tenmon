# -*- coding: utf-8 -*-
# Filename: reportinterface by: andrek
# Timesamp:2018-10-31 :: 12:52 using PyCharm

import src.utils.three2two as three2two
from abc import abstractmethod, ABCMeta
from src import di

logger = di.get("Logger")


class ReportInterface:
	__metaclass__ = ABCMeta
	"""
	Interface for our Monitor UPDATE behaviour
	"""
	def __init__(self, *args, **kwargs):
		self.reporter_name = self.__class__.__module__[len('metric_'):]



	@abstractmethod
	def send_data(self, *args, **kwargs):
		"""
		Abstract class that needs to be implemented in all Monitors
		:param args: Optional list of Monitors to update
		:param kwargs: Optional list of KeyWord args
		:return: List of stats from all updated monitors
		"""
		pass

