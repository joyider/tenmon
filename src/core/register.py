# -*- coding: utf-8 -*-
# Filename: register by: andrek
# Timesamp:2020-04-15 :: 13:03 using PyCharm

import pulsar
import src.utils.jwt as jwt
import base64
import json

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
			print('Identifier Error - Wrong or wrongly formated key')


	def register(self, customerid, secret='secret', **kwargs):
		encoded = jwt.encode(kwargs, secret, algorithm='HS512', headers={'customerid': customerid})
		client = pulsar.Client('pulsar://127.0.0.1:6650')
		producer = client.create_producer('non-persistent://tenforward/clients/register', kwargs.get('clientid'))
		producer.send(encoded)
