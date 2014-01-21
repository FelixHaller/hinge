from hinge_modules.GUI import GUI
from hinge_modules.System import System


class Daemon():
	def __init__(self):
		self.gui = GUI()
		self.system = System(self.gui)

		self.gui.show()
