import os
import glob
import json
from collections import OrderedDict

import xmltodict
import pprint

from psycopg2 import connect, sql
from psycopg2.extras import DictCursor
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, AsIs

import pulsar

from src.config import BaseConfig as CONF
from src.utils.helpers import ParallelGenerator



class UnknownAuditType(TypeError):
	def __init__(self, message, type, *args):
		self.message = message
		self.type = type
		super(UnknownAuditType, self).__init__(message, type, *args)


class AuditLog:
	def __init__(self, audditdir=CONF.AUDIT_DIR):
		self.audit_directory = audditdir

	def _parse_audit_dict(self, auditdict):
		if type(auditdict) is OrderedDict:
			return [auditdict]
		elif type(auditdict) is list:
			return auditdict
		else:
			raise UnknownAuditType("Incorrect AuditRecord Type", type(auditdict['Audit']['AuditRecord']))


	def parse_audit_dir(self):
		print(self.audit_directory)

		for auditfile in glob.glob(self.audit_directory):
			#print(auditfile)
			afile = open(auditfile, 'r')
			auditdict = xmltodict.parse(afile.read())
			try:
				yield self._parse_audit_dict(auditdict['Audit']['AuditRecord'])
			except UnknownAuditType as e:
				pass


def main():
	a = AuditLog()
	#conn = connect(dbname='dbaudit', user='postgres', host='127.0.0.1', password='0oBSTinatenEss#maRyl7uMbeL0@3162')

	#conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # Most likely not needed
	#cursor = conn.cursor()

	client = pulsar.Client('pulsar://localhost:6650')
	producer = client.create_producer('my-topic')

	with ParallelGenerator(
		a.parse_audit_dir(),
		max_lookahead=100) as g:
		for data in g:
			for alog in data:
				producer.send(json.dumps(alog))
				#print(json.dumps({'payload': alog}))
				#insert = 'insert into csmp1 (%s) values %s'

				#l = [(c, v) for c, v in alog.items()]
				#columns = ','.join([t[0].lower() for t in l])
				#values = tuple([t[1] for t in l])
				#print(cursor.mogrify(insert, ([AsIs(columns)] + [values])))

	#cursor.close()

if __name__ == "__main__":
	main()
	print "Done"