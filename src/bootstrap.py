#
# Filename: bootstrap by: andrekarlsson
# Timesamp: 2018-11-05 :: 13:27

import platform
import sys
import signal
import threading
import time

from psutil import __version__ as psutil_version

from src import __author__, __license__, __version__, di
from src.client import Client, Reporter, Exms

# Check Python version
if sys.version_info < (2, 7) or (3, 0) <= sys.version_info < (3, 3):
	print('TenForward requires at least Python 2.7 or 3.3 to run.')
	sys.exit(1)

# Check PSutil version
psutil_min_version = (2, 0, 0)
psutil_version_info = tuple([int(num) for num in psutil_version.split('.')])
if psutil_version_info < psutil_min_version:
	print('PSutil 2.0 or higher is needed. Exiting...')
	sys.exit(1)


def __signal_handler(signal, frame):
	di.get("Logger").info("Caught CTRL-C will gracefully try to exit")
	sys.exit(0)


def main():
	# Log Sentinel and PSutil version
	di.get("Logger").info('Start Sentinel {}'.format(__version__))
	di.get("Logger").info('{} {} and PSutil {} detected'.format(
		platform.python_implementation(),
		platform.python_version(),
		psutil_version))


	#config = core.get_config()
	#args = core.get_args()

	# Catch the CTRL-C signal
	signal.signal(signal.SIGINT, __signal_handler)

	start() #(config=config, args=args)

def start():
	di.get("Logger").info("Starting Client..")

	client = Client()
	reporter = Reporter()
	exm = Exms()

	x = threading.Thread(target=client.loop, args=())
	x2 = threading.Thread(target=reporter.loop, args=())
	for thread in exm.loop():
		threading.Thread(target=thread.start, args=()).start()
	# print(exm.loop())
	di.get("Logger").info("Main    : before running thread")
	x.start()
	x2.start()
	# x3.start()

	# client.end()
