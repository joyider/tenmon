# -*- coding: utf-8 -*-
#
# Filename: alertmanager by: andrek
# Timesamp:2018-05-01 :: 11:11 using PyCharm

from src.utils.helpers import singleton
import  inspect

@singleton
class AlertManager:
	registered_monitores = {}
	counter = {}

	def __init__(self, name):
		self.registered_monitores.append(name)

	def check(self, parameter, value):
		stack = inspect.stack()
		monitor = stack[1][0].f_locals["self"].__class__.__name__
		print(self.registered_monitores[monitor].get(parameter))

		#if value >= self.registered_monitores[monitor].get(parameter):
		#	print("Got alert")
