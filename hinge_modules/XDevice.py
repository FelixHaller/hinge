__author__ = 'Felix Haller'

from hinge_modules.Helper import *
from subprocess import check_call, Popen, PIPE


class XDevice():
	def __init__(self):
		self._name = None
		self._orientation = None
		self.rotModes = ["normal", "left", "inverted", "right"]

	@property
	def orientation(self):
		#@todo eigentlich sollte ein getter keinen komplexeren code ausführen (readSettings)
		# is necessary to have an up-to-date state (that could have changed externaly) of the devices
		self._readSettings()
		return self._orientation

	@property
	def name(self):
		return self._name

	def _readSettings(self):
		"""
		Reads the current settings of the screen device.
		Information is obtained with the help of the "xrandr" command.

		"""
		output = Popen(["xrandr", "--current"], stdout=PIPE).communicate()[0]
		devices_raw = output.rstrip().split(b'\n')
		for line in devices_raw:
			#take everything before the braces, clean it up and split on spaces
			line = line.split(b'(')[0].rstrip().split(b' ')
			if line[0] == b'LVDS1':
				self._name = line[0]
				if line[-1].decode("utf-8") in self.rotModes:
					self._orientation = line[-1]
				else:
					self._orientation = b'normal'


	def rotate(self, mode):
		"""
		Rotate the Screen. In fact we call "xrandr" with the -o option and an integer from 0-3

		:param mode: possible values 0,1,2,3 (for [normal, left, inverted, right])
		:type mode: int
		"""
		Helper.sendSystemCall("xrandr", "-o", self.rotModes[mode])

