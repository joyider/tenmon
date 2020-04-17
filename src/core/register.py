# -*- coding: utf-8 -*-
# Filename: register by: andrek
# Timesamp:2020-04-15 :: 13:03 using PyCharm

import pulsar
import src.utils.jwt as jwt
import base64
import json
import sys, time
import threading

from src.utils import minimaluuid


class Register:
	def __init__(self, token, **kwargs):
		self.kwargs = kwargs
		self.kwargs.update({'clientid': str(minimaluuid.uuid())})
		try:
			self.secret = json.loads(base64.b64decode(token))
			self.customerid = self.secret.get('customerid')
			self.secret = self.secret.get('uniquekey')
			self.register(self.customerid, secret=self.secret, **self.kwargs)
		except:
			print('Identifier Error - Incorrect or wrongly formated key')


	def register(self, customerid, secret='secret', **kwargs):
		encoded = jwt.encode(kwargs, secret, algorithm='HS512', headers={'customerid': customerid})
		sub = threading.Thread(target=self._client_sub, kwargs=({'clientid': kwargs.get('clientid')}))
		sub.start()
		time.sleep(2)
		client = pulsar.Client('pulsar://127.0.0.1:6650')
		producer = client.create_producer('non-persistent://tenforward/clients/register', kwargs.get('clientid'))
		producer.send(encoded)
		time.sleep(11)
		sub.do_run = False
		sub.join()
		sys.exit()


	def _client_sub(self, clientid=None):
		clientname = "{} Tenmon client".format(clientid)
		client = pulsar.Client('pulsar://127.0.0.1:6650')
		consumer = client.subscribe('persistent://tenforward/clients/{}'.format(clientid), clientname)
		t = threading.currentThread()
		while getattr(t, "do_run", True):
			try:
				msg = consumer.receive(timeout_millis=9000)
			except:
				client.close()
				sys.exit()
			try:
				#token = msg.data()
				#header = jwt.get_unverified_header(token)
				# print(jwt.decode(token, verify=False))
				#print(Register(header, token).verify_token())
				print("Received message '{}' id='{}'".format(msg.data(), msg.message_id()))
				# Acknowledge successful processing of the message
				consumer.acknowledge_cumulative(msg)
			except:
				# Message failed to be processed
				print("Signature missmatch")
				consumer.negative_acknowledge(msg)
		sys.exit(0)
