from WacomDevice import *

__author__ = 'Felix Haller'

class Stylus(WacomDevice):
	def __init__(self, name: str):
		WacomDevice.__init__(self, name)



	def isHover(self):
		status = None
		output = Popen(["xinput", "list-props", self.name], stdout=PIPE).communicate()[0]

		for line in output.split(b'\n'):
			if b'Wacom Hover Click' in line:
				status = int(line.split(b':')[1].decode("UTF-8").strip())

		if (status == 1):
			return(True)
		elif (status == 0):
			return(False)
		else:
			print("can not get hover-click status of" + self.name)

	def setHoverClick(self, mode):
		Helper.sendSystemCall('xinput', 'set-prop', self.name, 'Wacom Hover Click', mode)