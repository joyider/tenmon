# -*- coding: utf-8 -*-
# Filename: register by: andrek
# Timesamp:2020-04-15 :: 13:03 using PyCharm

import pulsar
import src.utils.jwt as jwt

from src.utils import minimaluuid


class Register:
	def __init__(self, secret, **kwargs):
		self.clientid = minimaluuid.uuid()
		self.register(self.clientid, secret=secret, **kwargs)


	def register(self, clientid, secret='secret', **kwargs):
		print("sertect is: {}".format(secret))
		encoded = jwt.encode(kwargs, secret, algorithm='HS512', headers={'clientid': clientid})
		client = pulsar.Client('pulsar://127.0.0.1:6650')
		producer = client.create_producer('non-persistent://tenforward/clients/register', 'apan')
		print(encoded)
		producer.send(encoded)
