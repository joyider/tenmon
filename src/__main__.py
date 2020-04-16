#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from . import di
import src.bootstrap
from src.core import register
#from os.path import pardir, realpath

#sys.path.append(realpath(pardir))
#print(sys.path)


if __name__ == '__main__':
	import argparse  # noqa
	parser = argparse.ArgumentParser(description='Tenforward Moniter')
	parser.add_argument('-r', '--register', nargs='?', default=False, const='aV3ryS3cr3tPassw0rd',
	help='Register the client to central store Using supplied key')
	args = parser.parse_known_args()
	if args[0].register:
		register.Register(args[0].register, hostname=di.get_variable('hostname'),
		         ip=di.get_variable('ip'), platform=di.get_variable('platform'), cpucount= di.get('CpuMeter').get()[1])

		sys.exit()

	src.bootstrap.main()
