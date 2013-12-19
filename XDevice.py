__author__ = 'Felix Haller'

from Helper import *
from subprocess import check_call, Popen, PIPE


class XDevice():
	def __init__(self):
		self.name = ""
		self.orientation = ""
		self.rotModes = ["normal", "left", "inverted", "right"]

	def readSettings(self):
		output = Popen(["xrandr", "--current"], stdout=PIPE).communicate()[0]
		devices_raw = output.rstrip().split(b'\n')
		devices = []
		for line in devices_raw:
			#take everything before the braces, clean it up and split on spaces
			line = line.split(b'(')[0].rstrip().split(b' ')
			if line[0] == b'LVDS1':
				self.name = line[0]
				if line[-1].decode("utf-8") in self.rotModes:
					self.orientation = line[-1]
				else:
					self.orientation = b'normal'
	def getOrientation(self):
		self.readSettings()
		return self.orientation


	def rotate(self, mode: int):
		Helper.sendSystemCall("xrandr", "-o", self.rotModes[mode])

