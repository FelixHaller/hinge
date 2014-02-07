from hinge_modules.System import System
from hinge_modules.gui.Indicator import Indicator


class GUI():
	def __init__(self):
		self.core = System()
		self.gui = Indicator(self.core)
