__author__ = 'Felix Haller'

from Helper import *

class WacomDevice:
    def __init__(self, name: str):
        self.name = name
        self.rotModes = {0: "none", 2: "half"}

    def getDeviceName(self):
        return (self.name)

    def rotate(self, mode :int):
        Helper.sendSystemCall('xsetwacom', '--set', self.name, 'rotate', self.rotModes[mode])

    def getOrientation(self):
        """Used to get the current orientation of a device."""
        pass

    def disable(self):
        print("disable...")

    #self.sendWacomSystemCall('--set', self.name, 'touch', 'off')

    def enable(self):
        print("enable...")

        #self.sendWacomSystemCall('--set', self.name, 'touch', 'on')


