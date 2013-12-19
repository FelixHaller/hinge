#!/usr/bin/python3

import sys, getopt
from Daemon import Daemon
from System import System


def main(argv):
	if (len(sys.argv) > 1):
		CLIArgs = sys.argv[1:]
		try:
			opts, args = getopt.getopt(CLIArgs,"hO:odfT:t",["flip", "daemon", "help", "Touch=", "toogle-touch", "Hover-click=", "toggle-hover-click"])
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
				System().rotateDevices()
			elif opt in ("-T", "--Touch"):
				if arg in ("on", "off"):
					System().tglFingerTouch(mode=arg)
				else:
					printHelp()
					sys.exit(2)
			elif opt in ("-t", "--toggle-touch"):
				print("toggeling...")
				System().tglFingerTouch()
			elif opt in ("-O", "--Hover-click"):
				if arg in ("on", "off"):
					System().tglHoverClick(mode={"off":"0","on":"1"}[arg])
				else:
					printHelp()
					sys.exit(2)
			elif opt in ("-o", "--toggle-hover-click"):
				print("toggeling hover-click...")
				System().tglHoverClick()
	else:
		printHelp()
def printHelp():
	print(
	'''You can use this tool either as a CLI to perform some actions, or start it as a daemon with an indicator/systray menu

-d                             start daemon
-f, --flip                     flip the rotation of the screen (rotate 180°)
-T, --Touch <on,off>           enable/disable finger touch input
-t, --toggle-touch             toggle finger touch input
-O, --Hover-click <on,off>     enable/disable wacom hover click
-o, --toggle-hover-click       toggle wacom hover click
''')

if __name__ == "__main__":
	main(sys.argv)