#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Authors: Felix Haller <ich@ein-freier-mensch.de>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of either or both of the following licenses:
#
# 1) the GNU Lesser General Public License version 3, as published by the
# Free Software Foundation; and/or
# 2) the GNU Lesser General Public License version 2.1, as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the applicable version of the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of both the GNU Lesser General Public
# License version 3 and version 2.1 along with this program.  If not, see
# <http://www.gnu.org/licenses/>
#


import sys, getopt
from Daemon import Daemon
from System import System


def main(argv):
	if (len(sys.argv) > 1):
		CLIArgs = sys.argv[1:]
		try:
			opts, args = getopt.getopt(CLIArgs,"hO:odfT:twnr:",["flip", "daemon", "help", "Touch=",
																"toogle-touch", "Hover-click=", "toggle-hover-click",
																"writing", "normal", "Rotate="])
		except getopt.GetoptError:
			printHelp()
			sys.exit(2)
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				printHelp()
				sys.exit()
			elif opt in ("-d", "--daemon"):
				Daemon()
			elif opt in ("-f", "--flip"):
				System().rotateDevices()
			elif opt in ("-r", "--Rotate"):
				if arg in ("normal","left","right","inverted"):
					System().rotateDevices(mode={"normal":0,"left":1,"inverted":2,"right":3}[arg])
			elif opt in ("-T", "--Touch"):
				if arg in ("on", "off"):
					System().tglFingerTouch(mode=arg)
				else:
					printHelp()
					sys.exit(2)
			elif opt in ("-t", "--toggle-touch"):
				System().tglFingerTouch()
			elif opt in ("-O", "--Hover-click"):
				if arg in ("on", "off"):
					System().tglHoverClick(mode={"off":"0","on":"1"}[arg])
				else:
					printHelp()
					sys.exit(2)
			elif opt in ("-o", "--toggle-hover-click"):
				System().tglHoverClick()
			elif opt in ("-w", "--writing"):
				s = System()
				s.tglHoverClick(mode="1")
				s.tglFingerTouch(mode="off")
				s.rotateDevices()
			elif opt in ("-n", "--normal"):
				s = System()
				s.rotateDevices(mode=0)
				s.tglHoverClick(mode="0")
				s.tglFingerTouch(mode="on")

	else:
		printHelp()
def printHelp():
	print(
	'''convertible-tool 0.0.1
2013 Felix Haller <ich@ein-freier-mensch.de>

You can use this tool either as a CLI to perform some actions, or start
it as a daemon with an indicator/systray menu.

parameters:
-d                             start daemon
-f, --flip                     flip the rotation of the screen (rotate 180°)
-T, --Touch on,off             enable/disable finger touch input
-t, --toggle-touch             toggle finger touch input
-O, --Hover-click on,off       enable/disable wacom hover click
-o, --toggle-hover-click       toggle wacom hover click
-n, --normal                   reset settings to default
-r, --rotate <orientation>     set a specific orientation (absolute)
                               possible values: normal, left, right, inverted
''')

if __name__ == "__main__":
	main(sys.argv)