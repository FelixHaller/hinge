__author__ = 'felix'
from Helper import *

class WacomDevice:
    def __init__(self, name: str):
        self.name = name
        self.rotModes = {0: "none", 90: "foo", 180: "half"}

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

class Eraser(WacomDevice):
    def __init__(self, name: str):
        """
        Bli Bla Blubber
        """
        WacomDevice.__init__(self, name)


class Stylus(WacomDevice):
    def __init__(self, name: str):
        WacomDevice.__init__(self, name)


class Touch(WacomDevice):
    def __init__(self, name: str):
        WacomDevice.__init__(self, name)
