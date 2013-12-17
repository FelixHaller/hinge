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

from WacomDevice import *
from GUI import *
from XDevice import *


class Start():
	def __init__(self):
		self.system = System()
		self.gui = GUI()
		self.buildGUIMenu()
		self.gui.show()


	def rotateDevices(self, item, mode=None):
		if mode == None:
			#entering automatic mode
			if self.system.display.getOrientation() == b'inverted':
				mode = 0
			else:
				mode = 180
		for device in self.system.devices:
			device.rotate(mode)

	def buildGUIMenu(self):

		# add rotate entry
		self.gui.addMenuEntry(self.gui.menu, "rotate 180°").connect("activate", self.rotateDevices)



if __name__ == "__main__":
	Start()
