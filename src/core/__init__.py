# -*- coding: utf-8 -*-
#
# Filename: __init__.py by: andrek
# Timesamp: 2018-10-24 :: 12:10

import pulsar

def register():
	client = pulsar.Client('pulsar://127.0.0.1:6650')
	producer = client.create_producer('persistent://tenforward/clients/register', 'apan')
	print("Registering")
	producer.send("Register ME")
