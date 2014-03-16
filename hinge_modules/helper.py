__author__ = 'Felix Haller'

from subprocess import check_call, CalledProcessError


class Helper():
	@staticmethod
	def sendSystemCall(command: str, *args: str):
		"""
		handles systems calls
		"""
		cmdLine = []
		cmdLine.append(command)

		for arg in args:
			cmdLine.append(arg)

		if "debug1" == "debug":
			print("executing system command: ", end="")
			for part in cmdLine:
				#@todo: Warum zur Hölle verschwindet die Ausgabe, wenn ich hinter den Part auch ein end="" packe?
				print(part)
		try:
			check_call(cmdLine)
			return True
		except CalledProcessError as ex:
			print(ex)
			return False
		except FileNotFoundError:
			return False


