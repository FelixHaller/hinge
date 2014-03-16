import logging
from hinge_modules.helper import *
from subprocess import Popen, PIPE

__author__ = 'Felix Haller'

class WacomDevice:
	def __init__(self, name: str):
		self._name = name
		self._rotModes = ["none", "ccw", "half", "cw"]
		self._orientation = None
		self._isEnabled = False

	@property
	def name(self):
		return self._name

	@property
	def isEnabled(self):
		self._readStatus()
		return self._isEnabled

	@property
	def orientation(self):
		"""
		Used to get the current orientation of a device.
		"""
		self._readOrientation()
		return self._orientation

	def rotate(self, mode:int):
		try:
			Helper.sendSystemCall('xsetwacom', '--set', self._name, 'rotate', self._rotModes[mode])
		except:
			raise


	def switch(self, mode:int):
		try:
			Helper.sendSystemCall('xsetwacom', '--set', self._name, 'touch', {0: "off", 1: "on"}[mode])
		except:
			raise

	def _readSettings(self):
		self._readStatus()
		self._readOrientation()


	def _readStatus(self):
		try:
			result = self._readValue("touch")
		except:
			logging.error("could not get status of " + self._name)
			self._isEnabled = False
			raise
			return
		if result == "on":
			self._isEnabled = True
		else:
			self._isEnabled = False

	def _readOrientation(self):
		try:
			self._orientation = self._readValue("rotate")
		except:
			logging.ERROR("could not get orientation of " + self._name)
			return

	def _readValue(self, value):
		try:
			return Popen(["xsetwacom", "--get", self._name, value], stdout=PIPE).communicate()[0].decode("UTF-8").strip()
		except:
			raise

class Touch(WacomDevice):
	def __init__(self, name: str):
		WacomDevice.__init__(self, name)

class Stylus(WacomDevice):
	def __init__(self, name: str):
		WacomDevice.__init__(self, name)

	def isHover(self):
		status = None
		output = Popen(["xinput", "list-props", self._name], stdout=PIPE).communicate()[0]

		for line in output.split(b'\n'):
			if b'Wacom Hover Click' in line:
				status = int(line.split(b':')[1].decode("UTF-8").strip())

		if status == 1:
			return True
		elif status == 0:
			return False
		else:
			#@todo sollte hier auch irgendeinen return code geben
			logging.critial("can not get hover-click status of" + self._name)

	def setHoverClick(self, mode):
		if Helper.sendSystemCall('xinput', 'set-prop', self._name, 'Wacom Hover Click', {0:"0", 1:"1"}[mode]):
			pass
		else:
			logging.critial("Error when trying to set Hover click")

class Eraser(WacomDevice):
	def __init__(self, name: str):
		"""
		Bli Bla Blubber
		"""
		WacomDevice.__init__(self, name)