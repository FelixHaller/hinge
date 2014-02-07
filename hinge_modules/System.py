from subprocess import check_call, Popen, PIPE
import sys, signal, logging
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

	def __init__(self):
		"""
		It's possible to create a System object with or without having a GUI() object.
		If one is given the Menus will be created depending on which features the System
		supports and what devices it has.

		:param gui: a reference to the created GUI (indicator, tray icon, ...)
		:type gui: GUI.GUI
		"""
		self.devices = []


		# the XDevice will allways be generated
		self._display = XDevice()

		#These are these potentially possible devices
		self._touchDev = None
		self._eraserDev = None
		self._stylusDev = None

		#add the display device to the devices list
		self.devices.append(self._display)

		#and retrieve all wacom devices
		self._retrWacomDeviceNames()
	@property
	def touchDev(self):
		return self._touchDev

	@property
	def stylusDev(self):
		return self._stylusDev

	@property
	def eraserDev(self):
		return self._eraserDev

	def hasDevices(self):
		return(self.devices.__len__() > 0)

	def _retrWacomDeviceNames(self):
		"""
		Get the details of all connected Wacom Devices by using the "xsetwacom" command.
		"""
		logging.info("retrieving Devices")
		wacomDevices = []
		try:
			output = Popen(["xsetwacom", "--list", "devices"], stdout=PIPE).communicate()[0]
		except FileNotFoundError:
			logging.error("'xsetwacom' command not found. Please install and try again")
			sys.exit(-1)
		if len(output) == 0:
			return

		for line in output.rstrip().split(b'\n'):
			wacomDevices.append(line.split(b'\t'))

		for entry in wacomDevices:
			if 'STYLUS' in entry[2].decode("utf-8"):
				logging.info("stylus device found...")
				self._stylusDev = Stylus(entry[0].rstrip().decode("UTF-8"))
				self.devices.append(self._stylusDev)
			elif 'ERASER' in entry[2].decode("utf-8"):
				logging.info("eraser device found...")
				self._eraserDev = Eraser(entry[0].rstrip().decode("UTF-8"))
				self.devices.append(self._eraserDev)
			elif 'TOUCH' in entry[2].decode("utf-8"):
				logging.info("touch device found...")
				self._touchDev = Touch(entry[0].rstrip().decode("UTF-8"))
				self.devices.append(self._touchDev)


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
			if self._display.orientation == b'normal':
				mode = 2
			else:
				mode = 0
		for device in self.devices:
			try:
				device.rotate(mode)
			except:
				logging.critical("error while rotating the device")


	def tglFingerTouch(self, menuItem=None, mode:int=None):
		"""
		Turn the touch feature of your wacom device on or off. If no mode is given then toggle.

		:type menuItem: Gtk.MenuItem
		:param menuItem: given by the GUI, when a button is pressed
		:param mode: turn it on(1) or off(0)
		:type mode: int
		"""

		if self.hasTouchDev():
			if menuItem is not None:
				mode = int(menuItem.get_active())
			if mode is not None:
				self._touchDev.switch(mode)
			else:
				self._touchDev.switch(not self._touchDev.isEnabled)
		logging.warning("FINGER " + str(mode))
	def tglHoverClick(self, menuItem=None, mode:int=None):
		"""
		Turn the "hover click" feature of your wacom stylus device on or off. If no mode is given then toggle.

		:type menuItem: Gtk.MenuItem
		:param menuItem: given by the GUI, when a button is pressed
		:param mode: turn it on(1) or off(0)
		:type mode: int
		"""

		if self.hasStylusDev():
			if menuItem is not None:
				mode = int(menuItem.get_active())
			if mode is not None:
				self._stylusDev.setHoverClick(mode)
			else:
				status = self._stylusDev.isHover()
				if status:
					self._stylusDev.setHoverClick(0)
				elif not status:
					self._stylusDev.setHoverClick(1)
		logging.warning("HOVER "+ str(mode))

	def normalMode(self, menuItem=None):
		"""
		Activates the normal mode:
		- normal display/input devices orientation
		- HoverClick disabled
		- Touch input enabled

		:param sysObj: has to be an instance of hinge_modules.System.System()
		"""
		self.rotateDevices(mode=0)
		self.tglHoverClick(mode=0)
		self.tglFingerTouch(mode=1)

	def tglWritingMode(self, menuItem=None, mode=None):
		"""
		This is a helper function to make it possible to toggle the writing mode
		(my favorite).
		The decision which mode to choose depends on the current display orientation.
		Only if it's in the "normal" state the writing mode will be applied. any other state
		will lead to the normal mode (-n) to be applied.

		:param sysObj: has to be an instance of hinge_modules.System.System()
		:param mode: either 1 or 0 or None for toggeling
		"""
		if mode is None:
			if self._display.orientation == b'normal':
				mode = 1
			else:
				self.normalMode()
				return
		self.tglHoverClick(mode=mode)
		self.tglFingerTouch(mode={0:1,1:0}[mode])
		self.rotateDevices(mode={0: 0, 1: 2}[mode])

	def hasStylusDev(self):
		return (self._stylusDev is not None)


	def hasEraserDev(self):
		return (self._eraserDev is not None)


	def hasTouchDev(self):
		return (self._touchDev is not None)