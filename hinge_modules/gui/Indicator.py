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
			"/home/felix/Design/icons/hinge/hinge.svg", # standard icon
			AppIndicator3.IndicatorCategory.HARDWARE)
		self.menu = Menu()
		self.buttonHandlers = {}
		self.headerLabel = HeaderLabel("Tablet Indicator")

		self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
		self.ind.set_menu(self.menu)
		self.menu.append(self.headerLabel)

		self._addMenus()

		self._show()

	def _addMenus(self):
		"""
		Add rotate entry if there is any device (X, stylus, etc...)
		however....there should be at least the XDevice.
		"""

		#todo: at the moment every set_Active() methods cause an unnecessary system-call to be executed.
		#(it seems the event is triggered). But I do need to set the menuButtons checked anyhow.
		if not self.core.hasDevices():

			self._setHeaderLabel("Error: no devices found")
			return

		else:
			# add the separator first and put all toggles above and all regular buttons below
			separator = Gtk.SeparatorMenuItem()
			separator.show()

			self.menu.add(separator)

			# create the "orientation" subMenu
			self.rotate = self._addSubMenu("orientation")

			self.rotateN = self._addMenuItem(self.rotate, "normal", self.core.rotateDevices, 0)
			self.rotateL = self._addMenuItem(self.rotate, "left", self.core.rotateDevices, 1)
			self.rotateI = self._addMenuItem(self.rotate, "flipped", self.core.rotateDevices, 2)
			self.rotateR = self._addMenuItem(self.rotate, "right", self.core.rotateDevices, 3)

			self.normal = self._addMenuItem(self.menu, "-> normal mode", self._normalHandler)


		# if there is a touch device add a menu to en/disable the touch input
		if self.core.hasTouchDev():
			self.tglTouch = self._addCheckMenuItem(self.menu, "Touch", self._touchHandler)
			self.tglTouch.set_active(self.core.touchDev.isEnabled)

		# if there is a stylus device add a menu to en/disable the hover click and the writing mode
		if self.core.hasStylusDev():
			self.tglHover = self._addCheckMenuItem(self.menu, "Hover-Click", self._hoverHandler)
			self.tglHover.set_active(self.core.stylusDev.isHover())

			self.writing = self._addMenuItem(self.menu, "-> enter writing-mode", self._writingHandler)

	def _hoverHandler(self, subMenu):
		self.core.tglHoverClick(menuItem = subMenu)

	def _touchHandler(self, subMenu):
		self.core.tglFingerTouch(menuItem = subMenu)

	def _writingHandler(self, subMenu):
		"""
		This method is the handler for the writing mode button.
		In contrast to the cli here we do not only call the core methods, as we need
		the CheckMenuItems (e.g. Hover-Click, Touch) to be (un)checked.

		:param subMenu:
		"""

		if self.core.hasStylusDev():
			# enable hover click
			self.tglHover.set_active(True)
			self.core.tglHoverClick(mode=1)

		if self.core.hasTouchDev():
			# disable the finger touch input
			self.tglTouch.set_active(False)
			self.core.tglFingerTouch(mode=0)

		# flip the screen
		self.rotateI.activate()

	def _normalHandler(self, subMenu):
		"""
		This method is the handler for the normal mode button.
		In contrast to the cli here we do not only call the core methods, as we need
		the CheckMenuItems (e.g. Hover-Click, Touch) to be (un)checked.

		:param subMenu:
		"""
		if self.core.hasStylusDev():
			#disable Hover-Click
			self.tglHover.set_active(False)
			self.core.tglHoverClick(mode=0)

		if self.core.hasTouchDev():
			# enable the finger touch input
			self.tglTouch.set_active(True)
			self.core.tglFingerTouch(mode=1)

		# flip the screen
		self.rotateN.activate()

	def _setHeaderLabel(self, caption):
		self.headerLabel.set_label(caption)


	def _addSubMenu(self, caption):
		"""
		Add a submenu to the main indicator menu.

		:param caption: caption of the new menu entry
		:return: a reference to the created menu
		:rtype: Gtk.MenuItem
		"""
		subMenu = Gtk.Menu()

		items = Gtk.MenuItem(label=caption)
		items.set_submenu(subMenu)
		items.show()

		self.menu.insert(items, -1)

		return subMenu

	def _addCheckMenuItem(self, subMenu, caption, callback):
		entry = CheckMenuItem(caption)
		handler = entry.connect("activate", callback)

		self.buttonHandlers[entry] = handler
		# put in position 1 (below the header)
		subMenu.insert(entry, 1)

		return entry

	def _addMenuItem(self, subMenu, caption, callback, *args):
		entry = MenuItem(caption)
		entry.connect("activate", callback, *args)

		# put in last position
		subMenu.insert(entry, -1)

		return entry

	def _show(self):
		Gtk.main()
