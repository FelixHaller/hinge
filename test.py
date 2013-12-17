__author__ = 'felix'

class Device():
    def __init__(self):
        self.eins = "Test"

class Kind1(Device):
    def __init__(self):
        Device.__init__(self)
        self.eins += "lol"
        print(self.eins)

Kind1()
