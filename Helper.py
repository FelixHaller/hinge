__author__ = 'felix'

from subprocess import check_call, Popen, PIPE

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

        if ("debug1" == "debug"):
            print("executing system command: ", end="")
            for part in cmdLine:
                #@todo: Warum zur Hölle verschwindet die Ausgabe, wenn ich hinter den Part auch ein end="" packe?
                print(part)

        check_call(cmdLine)
