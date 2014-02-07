from hinge_modules.gui.CheckMenuItem import CheckMenuItem
from hinge_modules.gui.Menu import Menu
from gi.repository import Gtk
from gi.repository import AppIndicator3
from hinge_modules.gui.HeaderLabel import HeaderLabel
import logging
from hinge_modules.gui.MenuItem import MenuItem

__author__ = 'Felix Haller'


class Indicator():
	"""
	An Indicator Menu (https://wiki.ubuntu.com/DesktopExperienceTeam/ApplicationIndicators) which is the "View"
	in a MCV - Concept.
	"""

	def __init__(self, core):
		"""
		The constructor ^^
		"""
		self.core = core
		self.ind = AppIndicator3.Indicator.new(
			"hinge", # indicator name
			"python", # standard icon
			AppIndicator3.IndicatorCategory.HARDWARE)
		self.menu = Menu()
		self.buttonHandlers = {}
		self.headerLabel = HeaderLabel("Tablet Indicator")

		self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
		self.ind.set_menu(self.menu)
		self.menu.append(self.headerLabel)

		self._addMenus()

		self.show()

	def _addMenus(self):
		"""
		Add rotate entry if there is any device (X, stylus, etc...)
		however....there should be at least the XDevice.
		"""

		#todo: at the moment every set_Active() methods cause an unnecessary system-call to be executed.
		#(it seems the event is triggered). But I do need to set the menuButtons checked anyhow.
		if not self.core.hasDevices():

			self.setHeaderLabel("Error: no devices found")
			return

		else:
			# add the separator first and put all toggles above and all regular buttons below
			separator = Gtk.SeparatorMenuItem()
			separator.show()

			self.menu.add(separator)

			# create the "orientation" subMenu
			self.rotate = self.addSubMenu("orientation")

			self.rotateN = self.addMenuItem(self.rotate, "normal", self.core.rotateDevices, 0)
			self.rotateL = self.addMenuItem(self.rotate, "left", self.core.rotateDevices, 1)
			self.rotateI = self.addMenuItem(self.rotate, "flipped", self.core.rotateDevices, 2)
			self.rotateR = self.addMenuItem(self.rotate, "right", self.core.rotateDevices, 3)

			self.normal = self.addMenuItem(self.menu, "-> normal mode", self.normalHandler)


		# if there is a touch device add a menu to en/disable the touch input
		if self.core.hasTouchDev():
			self.tglTouch = self.addCheckMenuItem(self.menu, "Touch", self.touchHandler)
			self.tglTouch.set_active(self.core.touchDev.isEnabled)

		# if there is a stylus device add a menu to en/disable the hover click and the writing mode
		if self.core.hasStylusDev():
			self.tglHover = self.addCheckMenuItem(self.menu, "Hover-Click", self.hoverHandler)
			self.tglHover.set_active(self.core.stylusDev.isHover())

			self.writing = self.addMenuItem(self.menu, "-> enter writing-mode", self.writingHandler)

	def hoverHandler(self, subMenu):
		self.core.tglHoverClick(menuItem = subMenu)

	def touchHandler(self, subMenu):
		self.core.tglFingerTouch(menuItem = subMenu)

	def writingHandler(self, subMenu):
		"""
		This method is the handler for the writing mode button.
		In contrast to the cli here we do not only call the core methods, as we need
		the CheckMenuItems (e.g. Hover-Click, Touch) to be (un)checked.

		:param subMenu:
		"""

		# enable hover click
		self.tglHover.set_active(True)
		self.core.tglHoverClick(mode=1)

		# disable the finger touch input
		self.tglTouch.set_active(False)
		self.core.tglFingerTouch(mode=0)

		# flip the screen
		self.rotateI.activate()

	def normalHandler(self, subMenu):
		"""
		This method is the handler for the normal mode button.
		In contrast to the cli here we do not only call the core methods, as we need
		the CheckMenuItems (e.g. Hover-Click, Touch) to be (un)checked.

		:param subMenu:
		"""
		#disable Hover-Click
		self.tglHover.set_active(False)
		self.core.tglHoverClick(mode=0)

		# enable the finger touch input
		self.tglTouch.set_active(True)
		self.core.tglFingerTouch(mode=1)

		# flip the screen
		self.rotateN.activate()

	def setHeaderLabel(self, caption):
		self.headerLabel.set_label(caption)


	def addSubMenu(self, caption):
		"""
		Add a submenu to the main indicator menu.

		:param caption: caption of the new menu entry
		:return: a reference to the created menu
		:rtype: Gtk.MenuItem
		"""
		subMenu = Gtk.Menu()

		items = Gtk.MenuItem(caption)
		items.set_submenu(subMenu)
		items.show()

		self.menu.insert(items, -1)

		return subMenu

	def addCheckMenuItem(self, subMenu, caption, callback):
		entry = CheckMenuItem(caption)
		handler = entry.connect("activate", callback)

		self.buttonHandlers[entry] = handler
		# put in position 1 (below the header)
		subMenu.insert(entry, 1)

		return entry

	def addMenuItem(self, subMenu, caption, callback, *args):
		entry = MenuItem(caption)
		entry.connect("activate", callback, *args)

		# put in last position
		subMenu.insert(entry, -1)

		return entry

	def show(self):
		Gtk.main()
