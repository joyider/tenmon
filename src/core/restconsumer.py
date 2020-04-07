# -*- coding: utf-8 -*-
# Filename: restconsumer by: andrek
# Timesamp:2018-11-05 :: 10:29 using PyCharm

import json
from src.utils.three2two import httplib2
from src.utils.helpers import singleton

from src import config


@singleton
class APIClient:
	def __init__(self):
		self.http = httplib2.Http()
		self.header = {'Authorization': 'Bearer %s' % (config.auth.jwt_token), 'Content-Type': 'application/json', 'User-Agent': 'Tenforward_Client'}
		print(self.header)

	def _http(self, url, method, header, body):
		response, content = self.http.request(url, method, headers=header, body=json.dumps(body))

		return response

	def send_data(self, url, body):
		self._http(url, 'POST', self.header, body)
