#!/usr/bin/python3

import sys, getopt
from Daemon import Daemon
from CLI import CLI


def main(argv):
	if (len(sys.argv) > 1):
		CLIArgs = sys.argv[1:]
		try:
			#@todo implement
			opts, args = getopt.getopt(CLIArgs,"hdf",["flip", "daemon", "help"])
		except getopt.GetoptError:
			printHelp()
			sys.exit(2)
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				printHelp()
				sys.exit()
			elif opt in ("-d", "--daemon"):
				print("starting daemon...")
				Daemon()
			elif opt in ("-f", "--flip"):
				print("flipping...")
				CLI()
	else:
		printHelp()
def printHelp():
	print(
	'''You can use this tool either as a CLI to perform some actions, or start it as a daemon with an indicator/systray menu

-d              start daemon
--flip          flip the rotation of the screen (rotate 180°)
	''')

if __name__ == "__main__":
	main(sys.argv)