# -*- coding: utf-8 -*-
#
# Filename: config by: andrek
# Timesamp:2018-10-28 :: 11:13 using PyCharm

from src.utils.three2two import ConfigParser
import sys
import os


class Config:
	class Section:
		def __init__(self, section_name, config):
			self.__section_name = section_name
			self.__config = config

		def __str__(self):
			return '%s: %s' % (self.__section_name, self.__config)

		def __getattr__(self, name):
			try:
				return self.__config.get(self.__section_name, name)
			except Exception as n_exp:
				print(('Can not find value for %s in config: %s\n' % (name, n_exp)))
				return None

		def set_attr(self, key, value):
			try:
				self.__config.set(self.__section_name, key, str(value))
			except Exception as n_exp:
				print(('Can not set value %s for %s to config: %s\n' % (value, key, n_exp)))

	def __init__(self, *args):
		self.__sections = dict()
		self.__config = ConfigParser(os.environ)
		self.add_config_ini(*args)

	def __getattr__(self, name):
		if name not in self.__sections:
			self.__sections[name] = self.Section(name, self.__config)
		return self.__sections[name]

	def add_config_ini(self, *args):
		list(map(lambda config_file_path: self.__config.read(config_file_path), args))
		self.__sections = dict(
			[(section, self.Section(section, self.__config)) for section in self.__config.sections()])


sys.modules[__name__] = Config()


def add_config_ini(*args):
	sys.modules[__name__].add_config_ini(*args)
