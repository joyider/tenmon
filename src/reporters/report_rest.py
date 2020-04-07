# -*- coding: utf-8 -*-
# Filename: report_rest by: andrek
# Timesamp:2018-11-07 :: 09:32 using PyCharm

import json
from src.utils.three2two import httplib2
from src.utils.helpers import singleton
from src.core.interfaces.reportinterface import ReportInterface

from src import config


class RestReporter(ReportInterface):
	class APIClient:
		def __init__(self):
			self.http = httplib2.Http()
			self.header = {'Authorization': 'Bearer %s' % (config.auth.jwt_token), 'Content-Type': 'application/json',
			               'User-Agent': 'Tenforward_Client'}
			print(self.header)

		def _http(self, url, method, header, body):
			response, content = self.http.request(url, method, headers=header, body=json.dumps(body))

			return response

		def send_data(self, url, body):
			self._http(url, 'POST', self.header, body)

	def __init__(self, config=None, *args, **kwargs):
		self.restclient = self.APIClient()
		super(RestReporter, self).__init__(config, *args, **kwargs)

	def send_data(self, report_data):
		#TODO: Raises Keyerror if failing Handle that exception
		table_name = report_data.pop('table_name', None)
		url = '%s/%s' % (config.reporting.url, table_name)
		print(url)
		resp = self.restclient.send_data(url, report_data)

		print(json.dumps(report_data))
		print(resp)

		return True if resp is None else False