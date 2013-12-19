__author__ = 'Felix Haller'

from Helper import *


class WacomDevice:
	def __init__(self, name: str):
		self.name = name
		self.rotModes = ["none", "ccw", "half", "cw"]

	def getDeviceName(self):
		return (self.name)

	def rotate(self, mode:int):
		Helper.sendSystemCall('xsetwacom', '--set', self.name, 'rotate', self.rotModes[mode])

	def getOrientation(self):
		"""
		Used to get the current orientation of a device.
		"""
		pass

	def turn(self, mode):
		Helper.sendSystemCall('xsetwacom', '--set', self.name, 'touch', mode)

	def isEnabled(self):
		status = Popen(["xsetwacom", "--get", self.name, "touch"], stdout=PIPE).communicate()[0].decode("UTF-8").strip()
		if (status == "on"):
			return(True)
		elif (status == "off"):
			return(False)
		else:
			print("can not get enabled/disabled status of" + self.name)