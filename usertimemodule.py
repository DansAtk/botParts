import pytz
import datetime
import sqlite3
import calendar

import commandsmodule
import config

includes = {}

time = commandsmodule.command('time', __name__)

def init():
    includes.update({time.name : time})
    time.description = "Time management."
    time.function = 'timeF'
    time.parameters.update({'set' : commandsmodule.command('set', __name__)})
    time.parameters['set'].description = "Sets the time."
    time.parameters['set'].function = 'setF'
    config.imports.append('usertimemodule')

def timeF(message):
    if len(message) > 0:
        print(time.paramError(message))
    else:
        print(getTime())

def setF(message):
    if len(message) > 0:
        print(time.parameters['set'].paramError(message))
    else:
        print("The time has been set.")

def getTime():
    return datetime.datetime.now().strftime("%H:%M:%S")

if __name__ == "__main__":
    print("Adds functionality for managing users located in different timezones. Should be merged into usermodule. No main.")
else:
    init()