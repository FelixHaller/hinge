from GUI import *
from System import *


class Daemon():
	def __init__(self):
		self.gui = GUI()
		self.system = System(self.gui)

		self.gui.show()




