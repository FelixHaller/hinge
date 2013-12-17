__author__ = 'Felix Haller'

from Helper import *
from subprocess import check_call, Popen, PIPE

class XDevice():
    def __init__(self):
        self.name = ""
        self.orientation = ""
        self.rotModes = {0: "normal", 90: "foo", 180: "inverted"}

    def readSettings(self):
        output = Popen(["xrandr", "--verbose"], stdout=PIPE).communicate()[0]
        devices_raw = output.rstrip().split(b'\n')
        devices = []
        for line in devices_raw:
            line = line.split(b' ')
            if line[0] == b'LVDS1' and line[2]==b'primary':
                self.name = line[0]
                self.orientation = line[5]

    def getOrientation(self):
        self.readSettings()
        return self.orientation


    def rotate(self, mode: int):
        Helper.sendSystemCall("xrandr", "-o", self.rotModes[mode])

