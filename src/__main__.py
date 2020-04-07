import sys
from os.path import pardir

sys.path.append(pardir)
from src.bootstrap import main

if __name__ == '__main__':
	print("Starting main")
	main()