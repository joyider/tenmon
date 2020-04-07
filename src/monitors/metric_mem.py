# -*- coding: utf-8 -*-
# Filename: metric_mem by: andrek
# Timesamp:2018-11-04 :: 13:31 using PyCharm

import collections
import os

from src.core.interfaces.updateinterface import UpdateInterface
from src import config
from src.utils.three2two import iteritems
from src.utils.chronometer import Counter

from src.core.alertmanager import AlertManager


from src import di

import psutil

logger = di.get("Logger")

class MemUpdate(UpdateInterface):

	"""TenForward CPU plugin.
	'stats' is a dictionary that contains the system-wide CPU utilization as a
	percentage.
	"""

	'''
	Default Alert levels custom made levels can be set from GUI
	Possible LEVELS are FATAL, CRITICAL, ERROR, WARNING, INFO
	'''
	ALERT_LEVELS = {'percent':
		                {'CRITICAL': 90, 'WARNING': 75}
	                }

	# Checks to send to remote DB
	NAMED_CHECKS = ['free', 'used']



	def __init__(self, *args, **kwargs):
		"""
		Do we need to call the superclass? i would prefer not to
		:param args: Optional args tuple
		:param kwargs: Optional KeyWord args dict
		"""
		super(MemUpdate, self).__init__(*args, **kwargs)
		self.prefix = self.__class__.__name__[:-6].lower()
		self.fn_for_db = os.path.basename(__file__)[:-3].lower()

		# Init stats
		self.reset()

		# Set initial value for CPU avarage
		self.mem_queue_len = int(int(config.reporting.freq)/int(config.checks.freq))
		self.mem_average = collections.deque(maxlen=self.mem_queue_len)


		# Counter for alert triggers
		self.tot_crit_counter = 0
		self.tot_warn_counter = 0

		self.warn_timer = Counter(autostart=False)
		self.crit_timer = Counter(autostart=False)


	def reset(self):
		"""Reset/init the stats."""
		self.stats = {}

	@UpdateInterface.result_logger
	def update(self):
		"""Update CPU stats using the input method."""

		# Reset stats
		self.reset()

		try:
			v_mem_stats = psutil.virtual_memory()
		except AttributeError:
			logger.error('Virtual_Memory only available with PSUtil 4.and above')
		else:
			for mem in ['total', 'available', 'percent', 'used', 'free',
			            'active', 'inactive', 'buffers', 'cached',
			            'wired', 'shared']:
				if hasattr(v_mem_stats, mem):
					self.stats[mem] = getattr(v_mem_stats, mem)

			# Use the 'free'/htop calculation
			# free=available+buffer+cached
			self.stats['free'] = self.stats['available']
			if hasattr(self.stats, 'buffers'):
				self.stats['free'] += self.stats['buffers']
			if hasattr(self.stats, 'cached'):
				self.stats['free'] += self.stats['cached']
			# used=total-free
			self.stats['used'] = self.stats['total'] - self.stats['free']

			if self.stats['percent'] >= self.ALERT_LEVELS['percent']['CRITICAL']:
				self.tot_crit_counter += 1
				if self.tot_crit_counter == 1:
					self.crit_timer.start()
			elif self.stats['percent'] >= self.ALERT_LEVELS['percent']['WARNING']:
				self.tot_warn_counter += 1
				if self.tot_warn_counter == 1:
					self.warn_timer.start()


			if self.tot_warn_counter >= 1 and self.warn_timer.get() > 20:
				logger.warning("Got Memory warning at %s percent, Warning Level is: %d" % (self.stats['percent'], self.ALERT_LEVELS['percent']['WARNING']))



			# Append to average FILO
			self.mem_average.append(self.stats)

		return self.stats


	def report(self):
		"""
		report check vaules ro be saved in remote DB
		:return: Dictionary with items to report
		{'MEM':
			{'free': 50,
			'used': 50
			...
			}
		}
		"""
		report_dict = collections.defaultdict(float)
		r_dict = collections.defaultdict(float)
		count = 1

		for mydict in self.mem_average:
			for key, value in iteritems(mydict):
				if key in MemUpdate.NAMED_CHECKS:
					report_dict[key] += value

		for key, value in iteritems(report_dict):
			r_dict[key] = value/self.mem_queue_len

		# Return the dict with CHECK Prefix
		return {'table_name': self.fn_for_db, self.prefix:  r_dict}
