from hinge_modules.system import *
from hinge_modules.ui.indicator import Indicator

class GUI():
	"""
	Creates a :class:`hinge_modules.system.System` and a :class:`hinge_modules.ui.indicator.Indicator` object.
	"""
	def __init__(self):
		self.core = System()
		self.gui = Indicator(self.core)
