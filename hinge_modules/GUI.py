__author__ = 'Felix Haller'

from gi.repository import Gtk
from gi.repository import AppIndicator3


class GUI():
	"""
	An Indicator Menu (https://wiki.ubuntu.com/DesktopExperienceTeam/ApplicationIndicators) which is the "View"
	in a MCV - Concept Model.
	"""
	def __init__(self):
		"""
		The constructor ^^
		"""
		self.ind = AppIndicator3.Indicator.new(
			"indicator-convertible", # indicator name
			"python", # standard icon
			AppIndicator3.IndicatorCategory.HARDWARE)
		self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
		self.menu = self.makeMenu()
		self.headerLabel = self.makeHeaderLabel("Tablet Indicator")

	def makeHeaderLabel(self, caption):
		"""


		:param caption: header caption
		:return: a reference to the headerLabel
		:rtype: Gtk.MenuItem
		"""
		headerLabel = Gtk.MenuItem()
		headerLabel.set_sensitive(False)
		headerLabel.set_label(caption)
		self.menu.append(headerLabel)
		headerLabel.show()
		return headerLabel

	def setHeaderLabel(self, caption):
		self.headerLabel.set_label(caption)

	def makeMenu(self):
		menu = Gtk.Menu()
		self.ind.set_menu(menu)
		return menu

	def addSubMenu(self, caption):
		"""
		Add a submenu to the main indicator menu.

		:param caption: caption of the new menu entry
		:return: a reference to the created menu
		:rtype: Gtk.MenuItem
		"""
		items = Gtk.MenuItem(caption)
		self.menu.append(items)
		subMenu = Gtk.Menu()
		items.set_submenu(subMenu)
		items.show()

		return subMenu

	def addMenuEntry(self, subMenu, caption):
		entry = Gtk.MenuItem(caption)
		subMenu.append(entry)
		entry.show()

		return entry


	def addActionToEntry(self, entry, callback):
		entry.connect("activate", callback)


	def show(self):
		Gtk.main()