__author__ = 'Felix Haller'

from subprocess import check_call, Popen, PIPE
from WacomDevice import *
from Eraser import *
from Stylus import *
from Touch import *
from XDevice import *

class System():
	"""
	This class handles everything that has to do with the system in general
	"""

	def __init__(self, gui=None):
		self.devices = []
		self.retrDeviceNames()
		self.gui = gui
		if self.gui != None:
			self.addMenusToGUI()

	def retrDeviceNames(self):
		output = Popen(["xsetwacom", "--list", "devices"], stdout=PIPE).communicate()[0]
		devices_raw = output.rstrip().split(b'\n')
		devices = []
		self.eraserDev = None
		self.stylusDev = None
		self.touchDev = None
		self.display = XDevice()
		self.devices.append(self.display)

		for line in devices_raw:
			devices.append(line.split(b'\t'))

		for entry in devices:
			if 'STYLUS' in entry[2].decode("utf-8"):
				self.stylusDev = Stylus(entry[0].rstrip().decode("UTF-8"))
				self.devices.append(self.stylusDev)
			elif 'ERASER' in entry[2].decode("utf-8"):
				self.eraserDev = Eraser(entry[0].rstrip().decode("UTF-8"))
				self.devices.append(self.eraserDev)
			elif 'TOUCH' in entry[2].decode("utf-8"):
				self.touchDev = Touch(entry[0].rstrip().decode("UTF-8"))
				self.devices.append(self.touchDev)


	def rotateDevices(self, menuItem=None, mode:int=None):
		if mode == None:
		#entering automatic mode
			if self.display.getOrientation() == b'inverted':
				mode = 0
			else:
				mode = 2
		for device in self.devices:
			device.rotate(mode)

	def addMenusToGUI(self):

		#  add rotate entry if there is any device (X, stylus, etc...)
		# however....there should be at least the XDevice
		if (len(self.devices) > 0):

			self.gui.addMenuEntry(self.gui.menu, "rotate 180°").connect("activate", self.rotateDevices)
		else:
			self.gui.setHeaderLabel("Error: no devices found")

		# if there is a touch device add an menu to en/disable the touch input
		if (self.touchDev != None):
			self.gui.addMenuEntry(self.gui.menu, "toggle Touch").connect("activate", self.tglFingerTouch)

		if (self.stylusDev != None):
			self.gui.addMenuEntry(self.gui.menu, "toggle Hover-Click").connect("activate", self.tglHoverClick)




	def tglFingerTouch(self, menuItem=None, mode=None):
		if self.touchDev != None:
			if mode == None:
				status = self.touchDev.isEnabled()
				if status:
					self.touchDev.turn("off")
				elif status == False:
					self.touchDev.turn("on")
			else:
				self.touchDev.turn(mode)

	def tglHoverClick(self, menuItem=None, mode:str=None):
		if self.stylusDev != None:
			if mode == None:
				status = self.stylusDev.isHover()
				if status:
					self.stylusDev.setHoverClick("0")
				elif status == False:
					self.stylusDev.setHoverClick("1")
			else:
				self.stylusDev.setHoverClick(mode)