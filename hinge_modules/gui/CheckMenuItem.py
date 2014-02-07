from gi.repository import Gtk

__author__ = 'Felix Haller'

class CheckMenuItem(Gtk.CheckMenuItem):
	def __init__(self, caption):
		super().__init__(caption)
		self.show()
