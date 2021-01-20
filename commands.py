# Classes and functions for organising available commands in each module.

import config
import sys

includes = {}

def init():
    config.imported.append('commands')
    print("\n")
class command:
    name = ""
    parent_module = ""
    def __init__(self, callname, module):
        self.name = callname
        self.parent_module = module
    description = ""
    function = ""
    parameters = {}
    enabled = True
    permlevel = 0

    def help(self):
        helptext = self.description + " Available parameters: "
        for param in self.parameters.values():
            helptext += param.name + ", "

        helptext += "help."
        return helptext
    def execute(self, additional):
        getattr(sys.modules[self.parent_module], self.function)(additional)

def parseCommand():
    print("parsing")
    return

def main():
    return

if __name__ == "__main__":
    main()
else:
    init()
    print("Commands module has been imported.")