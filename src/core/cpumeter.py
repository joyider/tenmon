# -*- coding: utf-8 -*-
# Filename: cpumeter by: andrek
# Timesamp:2018-01-18 :: 02:15 using PyCharm

from src.utils.chronometer import Chronometer

import psutil


class CpuMeter:
	"""Get and store the CPU percent."""

	def __init__(self, cached_time=1):
		self.cpu_usage = 0
		self.cpu_cores = {}
		self.percpu_percent = []

		# cached_time is the minimum time interval between stats updates
		# since last update is passed (will retrieve old cached info instead)
		self.timer_cpu = Chronometer(0)
		self.timer_percpu = Chronometer(0)
		self.cached_time = cached_time

	def get_key(self):
		"""Return the key of the per CPU list."""
		return 'cpu_number'

	def get(self, percpu=False):
		"""Update and/or return the CPU using the psutil library.
		If percpu, return the percpu stats"""
		if percpu:
			return self.__get_percpu(), self.__get_cores()
		else:
			return self.__get_cpu(), self.__get_cores()

	def __get_cpu(self):
		"""Update and/or return the CPU using the psutil library."""
		# Never update more than 1 time per cached_time
		if self.timer_cpu.finished():
			self.cpu_usage = psutil.cpu_percent(interval=0.0)
			# Reset timer for cache
			self.timer_cpu = Chronometer(self.cached_time)
		return self.cpu_usage

	def __get_cores(self):
		self.cpu_cores["phys"] = psutil.cpu_count(logical=False)
		self.cpu_cores["logical"] = psutil.cpu_count()
		return self.cpu_cores

	def __get_percpu(self):
		"""Update and/or return the per CPU list using the psutil library."""
		# Never update more than 1 time per cached_time
		if self.timer_percpu.finished():
			self.percpu_percent = []
			for cpu_number, cputimes in enumerate(psutil.cpu_times_percent(interval=0.0, percpu=True)):
				cpu = {'key': self.get_key(),
				       'cpu_number': cpu_number,
				       'total': round(100 - cputimes.idle, 1),
				       'user': cputimes.user,
				       'system': cputimes.system,
				       'idle': cputimes.idle}
				# The following stats are for API purposes only
				if hasattr(cputimes, 'nice'):
					cpu['nice'] = cputimes.nice
				if hasattr(cputimes, 'iowait'):
					cpu['iowait'] = cputimes.iowait
				if hasattr(cputimes, 'irq'):
					cpu['irq'] = cputimes.irq
				if hasattr(cputimes, 'softirq'):
					cpu['softirq'] = cputimes.softirq
				if hasattr(cputimes, 'steal'):
					cpu['steal'] = cputimes.steal
				if hasattr(cputimes, 'guest'):
					cpu['guest'] = cputimes.guest
				if hasattr(cputimes, 'guest_nice'):
					cpu['guest_nice'] = cputimes.guest_nice
				# Append new CPU to the list
				self.percpu_percent.append(cpu)
				# Reset timer for cache
				self.timer_percpu = Chronometer(self.cached_time)
		return self.percpu_percent