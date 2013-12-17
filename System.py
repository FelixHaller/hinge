__author__ = 'Felix Haller'

from subprocess import check_call, Popen, PIPE

class System():
	"""
	This class handles everything that has to do with the system in general
	"""
	def __init__(self):
		self.devices = []
		self.retrDeviceNames()

	def retrDeviceNames(self):
		output = Popen(["xsetwacom", "--list", "devices"], stdout=PIPE).communicate()[0]
		devices_raw = output.rstrip().split(b'\n')
		devices = []
		for line in devices_raw:
			devices.append(line.split(b'\t'))

		for entry in devices:
			if 'STYLUS' in entry[2].decode("utf-8"):
				self.stylusDev = Stylus(entry[0].rstrip().decode("UTF-8"))
				self.devices.append(self.stylusDev)
			elif 'ERASER' in entry[2].decode("utf-8"):
				self.eraserDev = Eraser(entry[0].rstrip().decode("UTF-8"))
				self.devices.append(self.eraserDev)
			elif 'TOUCH' in entry[2].decode("utf-8"):
				self.touchDev = Touch(entry[0].rstrip().decode("UTF-8"))
				self.devices.append(self.touchDev)

		self.display = XDevice()
		self.devices.append(self.display)