#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import src.bootstrap
from src.core import register
#from os.path import pardir, realpath

#sys.path.append(realpath(pardir))
print(sys.path)


if __name__ == '__main__':
	print("Starting main")
	import argparse  # noqa
	parser = argparse.ArgumentParser(description='Tenforward Moniter')
	parser.add_argument('-r', default=False,
	help='Register the client to central store Using supplied key')
	args = parser.parse_known_args()
	print(args)
	if args[0].r:
		register()
		sys.exit()

	src.bootstrap.main()
