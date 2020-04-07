# -*- coding: utf-8 -*-
# Filename: metric_cpu by: andrek
# Timesamp:2018-11-04 :: 12:04 using PyCharm

import collections
import os

from src.utils.chronometer import getTimeSinceLastUpdate
from src.core.interfaces.updateinterface import UpdateInterface
from src import config
from src.utils.three2two import iteritems


from src import di

logger = di.get("Logger")
cpumeter = di.get("CpuMeter")

import psutil


class CpuUpdate(UpdateInterface):

	"""TenForward CPU plugin.
	'stats' is a dictionary that contains the system-wide CPU utilization as a
	percentage.
	"""

	'''
	Default Alert levels custom made levels can be set from GUI
	Possible LEVELS are FATAL, CRITICAL, ERROR, WARNING, INFO
	'''
	ALERT_LEVELS = {'total':
		                {'CRITICAL': 90, 'WARNING': 75}
	                }

	# Checks to send to remote DB
	NAMED_CHECKS = ['total', 'iowait', 'softirq', 'ctx_switches', 'interrupts', 'soft_interrupts']

	def __init__(self, *args, **kwargs):
		"""
		Do we need to call the superclass? i would prefer not to
		:param args: Optional args tuple
		:param kwargs: Optional KeyWord args dict
		"""
		super(CpuUpdate, self).__init__(*args, **kwargs)
		self.prefix = self.__class__.__name__[:-6].lower()
		self.fn_for_db = os.path.basename(__file__)[:-3].lower()

		# Init stats
		self.reset()

		# Set initial value for CPU avarage
		self.cpu_queue_len = int(int(config.reporting.freq)/int(config.checks.freq))
		self.cpu_average = collections.deque(maxlen=self.cpu_queue_len)


		# Counter for alert triggers
		self.tot_crit_counter = 0
		self.tot_warn_counter = 0

		# Try to get the CPU Core count
		try:
			_, self.nb_core = cpumeter.get()
			self.nb_log_core = self.nb_core["logical"]
		except Exception:
			self.nb_log_core = 1

	def reset(self):
		"""Reset/init the stats."""
		self.stats = {}

	@UpdateInterface.result_logger
	def update(self):
		"""Update CPU stats using the PSUtil (aka. local)."""

		# Reset stats
		self.reset()

		# Grab stats into self.stats
		"""Update CPU stats using PSUtil."""
		# Grab CPU stats using psutil's cpu_percent and cpu_times_percent
		# Get all possible values for CPU stats: user, system, idle,
		# nice (UNIX), iowait (Linux), irq (Linux, FreeBSD), steal (Linux 2.6.11+)
		# The following stats are returned by the API but not displayed in the UI:
		# softirq (Linux), guest (Linux 2.6.24+), guest_nice (Linux 3.2.0+)
		self.stats['total'], _ = cpumeter.get()
		cpu_times_percent = psutil.cpu_times_percent(interval=0.0)
		for stat in ['user', 'system', 'idle', 'nice', 'iowait',
		             'irq', 'softirq', 'steal', 'guest', 'guest_nice']:
			if hasattr(cpu_times_percent, stat):
				self.stats[stat] = getattr(cpu_times_percent, stat)

		# Additionnal CPU stats (number of events / not as a %)
		# ctx_switches: number of context switches (voluntary + involuntary) per second
		# interrupts: number of interrupts per second
		# soft_interrupts: number of software interrupts per second. Always set to 0 on Windows and SunOS.
		# syscalls: number of system calls since boot. Always set to 0 on Linux.
		try:
			cpu_stats = psutil.cpu_stats()
		except AttributeError:
			logger.error('cpu_stats only available with PSUtil 4.1and above')
		else:
			# By storing time data we enable Rx/s and Tx/s calculations in the
			# XML/RPC API, which would otherwise be overly difficult work
			# for users of the API
			time_since_update = getTimeSinceLastUpdate('cpu')

			# Previous CPU stats are stored in the cpu_stats_old variable
			if not hasattr(self, 'cpu_stats_old'):
				# First call, we init the cpu_stats_old var
				self.cpu_stats_old = cpu_stats
			else:
				for stat in cpu_stats._fields:
					if getattr(cpu_stats, stat) is not None:
						self.stats[stat] = getattr(cpu_stats, stat) - getattr(self.cpu_stats_old, stat)

				self.stats['time_since_update'] = time_since_update

				# Core number is needed to compute the CTX switch limit
				self.stats['cpucore'] = self.nb_log_core

				# Save stats to compute next step
				self.cpu_stats_old = cpu_stats

			# Append to average FILO
			self.cpu_average.append(self.stats)

		return self.stats

	def report(self):
		"""
		report check vaules ro be saved in remote DB
		:return: Dictionary with items to report
		{'CPU':
			{'total': 35,
			'user': 22,
			'system': 13
			...
			...
			}
		}
		"""
		report_dict = collections.defaultdict(float)
		r_dict = collections.defaultdict(float)
		count = 1

		for mydict in self.cpu_average:
			for key, value in iteritems(mydict):
				if key in CpuUpdate.NAMED_CHECKS:
					report_dict[key] += value

		for key, value in iteritems(report_dict):
			r_dict[key] = value/self.cpu_queue_len

		#r_dict[]


		# Return the dict with CHECK Prefix
		return {'table_name': self.fn_for_db, self.prefix:  r_dict}
