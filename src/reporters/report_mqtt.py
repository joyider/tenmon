# -*- coding: utf-8 -*-
# Filename: report_rest by: andrek
# Timesamp:2020-04-04 :: 11:07 using PyCharm

import json

from src.utils.paho.mqtt.publish import single
import pulsar

from src.core.interfaces.reportinterface import ReportInterface

from src import config, di
logger = di.get('Logger')

# MQTT Settings

MQTT_Broker = "127.0.0.1"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "dummy"

DEBUG = True


class MqttReporter(ReportInterface):
	class Mqtt:
		@classmethod
		def publish_To_Topic(cls, topic, message, log=None):
			try:
			# pub = cls.mqttc.publish(topic, message, auth)
				pub = single(topic, message, hostname=MQTT_Broker, port=MQTT_Port)
				print("Publish to topic {} with  result: {}".format(str(topic), str(pub)))
			except Exception, e:
				print("Exception when publishing to topic {} with  exception: {}".format(str(topic), str(e)))
				return e

			if DEBUG:
				print("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))

			return pub

	def __init__(self, config=None, *args, **kwargs):
		print("In Mqtt")
		self.client = pulsar.Client('pulsar://127.0.0.1:6650')
		self.producer = self.client.create_producer('my-topic')
		super(MqttReporter, self).__init__(config, *args, **kwargs)

	def send_data(self, report_data):
		#TODO: Raises Keyerror if failing Handle that exception
		table_name = report_data.pop('table_name', None)
		# self.Mqtt.publish_To_Topic("/mqtt/test", report_data)
		self.producer.send(json.dumps(report_data))
		#resp = self.restclient.send_data(url, report_data)

		print(json.dumps(report_data))
		# print(resp)

		return True # if resp is None else False