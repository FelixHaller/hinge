__author__ = 'Felix Haller'

from gi.repository import Gtk
from gi.repository import AppIndicator3

class GUI():
	def __init__(self):
		self.ind = AppIndicator3.Indicator.new(
			"indicator-convertible", # indicator name
			"python", # standard icon
			AppIndicator3.IndicatorCategory.HARDWARE)
		self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
		self.menu = self.makeMenu()
		self.headerLabel = self.makeHeaderLabel()

	def makeHeaderLabel(self):
		headerLabel = Gtk.MenuItem()
		headerLabel.set_sensitive(False)
		headerLabel.set_label("Tablet Indicator")
		self.menu.append(headerLabel)
		headerLabel.show()
		return headerLabel

	def setHeaderLabel(self, caption: str):
		self.headerLabel.set_label(caption)

	def makeMenu(self):
		menu = Gtk.Menu()
		self.ind.set_menu(menu)
		return menu

	def addSubMenu(self, caption: str):
		"""
		adds a submenu to the main indicator menu. And returns a reference to it.

		@return: Gtk.Menu
		"""
		items = Gtk.MenuItem(caption)
		self.menu.append(items)
		subMenu = Gtk.Menu()
		items.set_submenu(subMenu)
		items.show()

		return subMenu


	def addMenuEntry(self, subMenu, caption: str):
		entry = Gtk.MenuItem(caption)
		subMenu.append(entry)
		entry.show()

		return entry


	def addActionToEntry(self, entry, callback):
		entry.connect("activate", callback)


	def show(self):
		Gtk.main()