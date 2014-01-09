from subprocess import check_call, Popen, PIPE
import sys
from hinge_modules.Eraser import Eraser
from hinge_modules.Stylus import Stylus
from hinge_modules.Touch import Touch
from hinge_modules.XDevice import XDevice

__author__ = 'Felix Haller'


class System():
	"""
	This class handles everything that has to do with the system in general.
	Actually it is our "controller" in a MCV - Concept Model.
	"""

	def __init__(self, gui=None):
		"""4
		It's possible to create a System object with or without having a GUI() object.
		If one is given the Menus will be created depending on which features the System
		supports and what devices it has.

		:param gui: a reference to the created GUI (indicator, tray icon, ...)
		:type gui: GUI.GUI
		"""
		self.display = XDevice()
		self.devices = []
		self.touchDev = None
		self.eraserDev = None
		self.stylusDev = None
		self.retrDeviceNames()
		self.gui = gui
		if self.gui is not None:
			self.addMenusToGUI()

	def retrDeviceNames(self):
		"""
		Get the details of all connected Wacom Devices by using the "xsetwacom" command.
		"""
		try:
			output = Popen(["xsetwacom", "--list", "devices"], stdout=PIPE).communicate()[0]
		except FileNotFoundError:
			print("'xsetwacom' command not found.")
			sys.exit(-1)
		devices_raw = output.rstrip().split(b'\n')
		devices = []

		self.devices.append(self.display)

		for line in devices_raw:
			devices.append(line.split(b'\t'))

		for entry in devices:
			if len(entry) != 3:
				print("unexpected entry format")
				continue

			if 'STYLUS' in entry[2].decode("utf-8"):
				self.stylusDev = Stylus(entry[0].rstrip().decode("UTF-8"))
				self.devices.append(self.stylusDev)
			elif 'ERASER' in entry[2].decode("utf-8"):
				self.eraserDev = Eraser(entry[0].rstrip().decode("UTF-8"))
				self.devices.append(self.eraserDev)
			elif 'TOUCH' in entry[2].decode("utf-8"):
				self.touchDev = Touch(entry[0].rstrip().decode("UTF-8"))
				self.devices.append(self.touchDev)

	def rotateDevices(self, menuItem=None, mode=None):
		"""
		Rotate all (input as well as output) devices to a specific orientation.
		When no mode is given, auto mode will rotate all devices to either normal
		or inverted orientation, depending on the current orientation of the display device.

		Example use case:
		  System().rotateDevices(1)    - rotate all devices to the "left" orientation
		  System().rotateDevices(0)    - rotate back to normal orientation
		  System().rotateDevices()     - (auto mode) rotate 180° to "inverted" in this case

		:param menuItem: given by the GUI, when a button is pressed
		:type menuItem: Gtk.MenuItem
		:param mode: 0, 1, 2 or 3 for normal, left, inverted or right orientation
		:type mode: int
		"""
		if mode is None:
			#entering automatic mode
			if self.display.getOrientation() == b'normal':
				mode = 2
			else:
				mode = 0
		for device in self.devices:
			device.rotate(mode)

	def addMenusToGUI(self):
		"""
		Add rotate entry if there is any device (X, stylus, etc...)
		however....there should be at least the XDevice.
		"""
		if len(self.devices) > 0:

			self.gui.addMenuEntry(self.gui.menu, "rotate 180°").connect("activate", self.rotateDevices)
		else:
			self.gui.setHeaderLabel("Error: no devices found")

		# if there is a touch device add an menu to en/disable the touch input
		if self.touchDev is not None:
			self.gui.addMenuEntry(self.gui.menu, "toggle Touch").connect("activate", self.tglFingerTouch)

		if self.stylusDev is not None:
			self.gui.addMenuEntry(self.gui.menu, "toggle Hover-Click").connect("activate", self.tglHoverClick)


	def tglFingerTouch(self, menuItem=None, mode=None):
		"""
		Turn the touch feature of your wacom device on or off. If no mode is given then toggle.

		:type menuItem: Gtk.MenuItem
		:param menuItem: given by the GUI, when a button is pressed
		:param mode: turn it "on" or "off"
		:type mode: str

		"""
		if self.touchDev is not None:
			if mode is None:
				status = self.touchDev.isEnabled()
				if status:
					self.touchDev.turn("off")
				elif status is False:
					self.touchDev.turn("on")
			else:
				self.touchDev.turn(mode)

	def tglHoverClick(self, menuItem=None, mode:str=None):
		"""
		Turn the "hover click" feature of your wacom stylus device on or off. If no mode is given then toggle.

		:type menuItem: Gtk.MenuItem
		:param menuItem: given by the GUI, when a button is pressed
		:param mode: turn it "on" or "off"
		:type mode: str
		"""
		if self.stylusDev is not None:
			if mode is None:
				status = self.stylusDev.isHover()
				if status:
					self.stylusDev.setHoverClick("0")
				elif not status:
					self.stylusDev.setHoverClick("1")
			else:
				self.stylusDev.setHoverClick(mode)