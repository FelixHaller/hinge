__author__ = 'Felix Haller'
from gi.repository import Gtk


class HeaderLabel(Gtk.MenuItem):
	def __init__(self, caption):
		"""

		:param caption: header caption
		"""

		super().__init__()
		self.set_sensitive(False)
		self.set_label(caption)
		self.show()