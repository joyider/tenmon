# -*- coding: utf-8 -*-
# Filename: __init__ by: andrekarlsson
# Timesamp: 2018-10-26 :: 13:30

import errno
import os
import sys
from Queue import Queue

import socket

import src.core.config as config
from src.utils.NoJoy_DI.di import DI
from src.utils.NoJoy_DI.patterns import BorgPattern, SingletonPattern, DefaultPattern

from src.utils.chronometer import Chronometer, Counter
from src.core.cpumeter import CpuMeter
from src.core.logger import Logger


config.add_config_ini('./src/config.ini')


# Global name
__version__ = '0.1'
__author__ = 'Andre Karlsson <andre.karlsson@protractus.com>'
__license__ = 'LGPLv3'

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


platforms = {
	'LINUX': sys.platform.startswith('linux'),
	'SUNOS': sys.platform.startswith('sunos'),
	'MACOS': sys.platform.startswith('darwin'),
	'BSD': sys.platform.find('bsd') != -1,
	'WINDOWS': sys.platform.startswith('win')
}

platform = next((k for k, v in platforms.items() if v is True), None)

work_path = os.path.realpath(os.path.pardir)
metrics_path = os.path.realpath(os.path.join(work_path, 'tenmon/src/monitors'))
reporters_path = os.path.realpath(os.path.join(work_path, 'tenmon/src/reporters'))
exm_path = os.path.realpath(os.path.join(work_path, 'tenmon/src/exm'))
sys.path.insert(0, metrics_path)
sys.path.insert(0, exm_path)
sys.path.insert(0, reporters_path)
sys_path = sys.path[:]


def safe_makedirs(path):
	"""A safe function for creating a directory tree."""
	try:
		os.makedirs(path)
	except OSError as err:
		if err.errno == errno.EEXIST:
			if not os.path.isdir(path):
				raise
		else:
			raise

"""
Create the Dependecy injector and attempt to add the needed classes
"""

di = DI()

di.attempt(Chronometer)
di.attempt(Counter)

# Add logger to di object as a Singleton
di.attempt(Logger, shared=True)

# Add The FIFO Queue to the DI object - One object Only
di.attempt(Queue, shared=True)

# Add the configuration as a Singleton
# di.attempt(Config, shared=True)

# Add basic monitoring for this HOST
di.attempt(CpuMeter, shared=True)

from src.core.reporter import Reporter  # noqa

di.attempt(Reporter, shared=True)

try:
	hostname = socket.gethostname()
	di.get(Logger).info("Hostname is: {}".format(hostname))
	print(hostname)
except:
	di.get(Logger).error("Unable to get hostname")
try:
	ip = get_ip_address()
	di.get(Logger).info("IP-Adress is: {}".format(ip))
	print(ip)
except:
	di.get(Logger).error("Unable to get IP adress")

di.add_variable('platform', platform)
di.add_variable('hostname', hostname)
di.add_variable('ip', ip)


def stop():
	di.get(Logger).info("Monitoring stopped by user")

# TODO: To be removed, using configparser
conf = config.BaseConfig
