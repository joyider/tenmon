# -*- coding: utf-8 -*-
# Filename: chronometer by: andrek
# Timesamp:2018-11-01 :: 00:03 using PyCharm

from time import time
from datetime import datetime

# Global list to manage the elapsed time
last_update_times = {}




def getTimeSinceLastUpdate(monitortype):
	"""
	Get time delta since last time monitor update
	:param monitortype: Monitor Type list on ['cpu','mem','disk]
	:return: actual time since last update for requested Monitor type
	"""
	#TODO Remove global
	global last_update_times
	current_time = time()
	last_time = last_update_times.get(monitortype)
	if not last_time:
		time_since_update = 1
	else:
		time_since_update = current_time - last_time
	last_update_times[monitortype] = current_time
	return time_since_update


class Chronometer:
	"""

	"""

	def __init__(self, duration):
		self.duration = duration
		self.start()

	def start(self):
		self.target = time() + self.duration

	def reset(self):
		self.start()

	def get(self):
		return self.duration - (self.target - time())

	def set(self, duration):
		self.duration = duration

	def finished(self):
		return time() > self.target


class Counter:
	"""

	"""

	def __init__(self, autostart=True):
		if autostart:
			self.start()

	def start(self):
		self.target = datetime.now()

	def reset(self):
		self.start()

	def get(self):
		return (datetime.now() - self.target).total_seconds()