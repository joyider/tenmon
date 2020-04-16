# -*- coding: utf-8 -*-
# Filename: logger by: andrek
# Timesamp:2017-10-03 :: 00:58 using PyCharm Community Edition

import logging
import os
import tempfile
from logging.handlers import RotatingFileHandler

# TODO: These should not be here as well consider Config location
LOGFILE = 'tenforward.log'
LOG_FILECOMPLETE = os.path.join(tempfile.gettempdir(), LOGFILE)
# print(LOG_FILECOMPLETE)


class _LoggerManager:
	def __init__(self, loggername):
		self.logger = logging.getLogger(loggername)
		rotatehandler = None

		try:
			rotatehandler = RotatingFileHandler(LOG_FILECOMPLETE,mode='a',
			                                    maxBytes=10485760,
			                                    backupCount=5
			                                    )
		except:
			raise IOError("Could not create/open the file {}, check permissions".format(LOG_FILECOMPLETE))

		self.logger.setLevel(logging.INFO)
		formater = logging.Formatter(
			fmt='[%(asctime)s] - [%(levelname)-8s] - %(message)s',
			datefmt='%F %H:%M:%S'
		)
		rotatehandler.setFormatter(formater)
		self.logger.addHandler(rotatehandler)

	def debug(self, loggername, message):
		self.logger = logging.getLogger(loggername)
		self.logger.debug(message)

	def error(self, loggername, message):
		self.logger = logging.getLogger(loggername)
		self.logger.error(message)

	def info(self, loggername, message):
		self.logger = logging.getLogger(loggername)
		self.logger.info(message)

	def warning(self, loggername, message):
		self.logger = logging.getLogger(loggername)
		self.logger.warning(message)

	def critical(self, loggername, message):
		self.logger = logging.getLogger(loggername)
		self.logger.critical(message)


class Logger:
	def __init__(self, loggername=LOGFILE):
		self.loggername = loggername
		self.logmanager = _LoggerManager(loggername)

	def debug(self, message):
		self.logmanager.debug(self.loggername, message)

	def error(self, message):
		self.logmanager.error(self.loggername, message)

	def info(self, message):
		self.logmanager.info(self.loggername, message)

	def warning(self, message):
		self.logmanager.warning(self.loggername, message)

	def critical(self, message):
		self.logmanager.critical(self.loggername, message)
