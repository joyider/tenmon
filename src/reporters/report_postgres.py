# -*- coding: utf-8 -*-
# Filename: report_rest by: andrek
# Timesamp:2018-11-07 :: 16:21 using PyCharm

import json
from src.utils.three2two import httplib2
from src.utils.helpers import singleton
from src.core.interfaces.reportinterface import ReportInterface

from src import config


class PostgresReporter(ReportInterface):

	def __init__(self, config=None, *args, **kwargs):
		print("In Postgres Reporter")
		super(PostgresReporter, self).__init__(config, *args, **kwargs)

	def send_data(self, report_data):
		#TODO: Raises Keyerror if failing Handle that exception
		table_name = report_data.pop('table_name', None)
		url = '%s/%s' % (config.reporting.url, table_name)
		print(url)
		#resp = self.restclient.send_data(url, report_data)

		print(json.dumps(report_data))
		# print(resp)

		return True # if resp is None else False