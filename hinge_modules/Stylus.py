from hinge_modules.WacomDevice import WacomDevice
from hinge_modules.Helper import Helper
from subprocess import Popen, PIPE
import logging


__author__ = 'Felix Haller'

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
