# -*- coding: utf-8 -*-
# Filename: report_rest by: andrek
# Timesamp:2020-04-04 :: 11:07 using PyCharm

import json

from src.utils.paho.mqtt.publish import single
import pulsar

from src.core.interfaces.reportinterface import ReportInterface

from src import config, di
logger = di.get('Logger')


class PulsarReporter(ReportInterface):

	def __init__(self, config=None, *args, **kwargs):
		self.client = pulsar.Client('pulsar://127.0.0.1:6650')
		self.producer = self.client.create_producer('my-topic')
		super(PulsarReporter, self).__init__(config, *args, **kwargs)

	def send_data(self, report_data):
		#TODO: Raises Keyerror if failing Handle that exception
		#table_name = report_data.pop('table_name', None)
		self.producer.send(json.dumps(report_data))

		return True # if resp is None else False