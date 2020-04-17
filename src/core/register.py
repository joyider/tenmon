# -*- coding: utf-8 -*-
# Filename: register by: andrek
# Timesamp:2020-04-15 :: 13:03 using PyCharm

import pulsar
import src.utils.jwt as jwt
import base64
import json
import sys, time
import pickle
import threading

from src.utils import minimaluuid


class Register:
	def __init__(self, token, **kwargs):
		self.kwargs = kwargs
		self.kwargs.update({'clientid': str(minimaluuid.uuid())})
		self.status = None
		self.clientid = None
		self.encoded = None
		try:
			self.secret = json.loads(base64.b64decode(token))
			self.customerid = self.secret.get('customerid')
			self.secret = self.secret.get('uniquekey')
			self.register(self.customerid, secret=self.secret, **self.kwargs)
		except Exception, e:
			print('Identifier Error - Incorrect or wrongly formated key: {}'.format(e))


	def register(self, customerid, secret='secret', **kwargs):
		self.clientid = kwargs.get('clientid')
		self.encoded = jwt.encode(kwargs, secret, algorithm='HS512', headers={'customerid': customerid})
		try:
			# File exists, registration is done atleaste once
			f = open("reg.b", "rb")
			oldencoded = pickle.load(f)
			try:
				oldclient = jwt.decode(oldencoded, secret, algorithms='HS512')
				print("Already Registered ")
				sys.exit()
				# return True, self.client
			except Exception, e:
				print("{}".format(e))
				# return False
		except IOError:
			print("No reg-file do register register")

		sub = threading.Thread(target=self._client_sub, kwargs=({'clientid': kwargs.get('clientid')}))
		sub.start()

		time.sleep(2)

		client = pulsar.Client('pulsar://127.0.0.1:6650')
		producer = client.create_producer('non-persistent://tenforward/clients/register', kwargs.get('clientid'))
		producer.send(self.encoded)

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
				self.status = json.loads(msg.data())
				print("Received message '{}' id='{}'".format(self.status, msg.message_id()))
				try:
					if self.status[self.clientid]:
						pickle.dump(self.encoded, open("reg.b", "wb"))
					else:
						print("Already Registered or Duplicate client")
				except KeyError, ke:
					print("Hmm Invalid Client Response")
				# Acknowledge successful processing of the message
				consumer.acknowledge_cumulative(msg)
			except Exception, e:
				# Message failed to be processed
				print("Signature missmatch: {}".format(e))
				consumer.negative_acknowledge(msg)
		sys.exit(0)
