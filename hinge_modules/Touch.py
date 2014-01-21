# -*- coding: utf-8 -*-
from hinge_modules.WacomDevice import WacomDevice

__author__ = 'Felix Haller'


class Touch(WacomDevice):
	def __init__(self, name: str):
		WacomDevice.__init__(self, name)