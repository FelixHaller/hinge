__author__ = 'Felix Haller'

from hinge_modules.Helper import *
from subprocess import Popen, PIPE



class WacomDevice:
	def __init__(self, name: str):
		self._name = name
		self._rotModes = ["none", "ccw", "half", "cw"]


	@property
	def name(self):
		return self._name


	def rotate(self, mode:int):
		Helper.sendSystemCall('xsetwacom', '--set', self._name, 'rotate', self._rotModes[mode])

	def getOrientation(self):
		"""
		Used to get the current orientation of a device.
		"""
		pass

	def turn(self, mode):
		Helper.sendSystemCall('xsetwacom', '--set', self._name, 'touch', mode)

	def isEnabled(self):
		try:
			status = Popen(["xsetwacom", "--get", self._name, "touch"], stdout=PIPE).communicate()[0].decode("UTF-8").strip()
		except:
			print("could not get enabled/disabled status of " + self._name)
			return False

		if status == "on":
			return True
		else:
			return False