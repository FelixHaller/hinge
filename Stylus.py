from WacomDevice import *

__author__ = 'Felix Haller'

class Stylus(WacomDevice):
	def __init__(self, name: str):
		WacomDevice.__init__(self, name)