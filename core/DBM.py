import sys
import os
import pathlib
import shutil

import sqlite3
import pytz
import calendar
from datetime import *

from core import config
from core.commandM import command

mSelf = sys.modules[__name__]
includes = {}
config.imports.append(__name__)

class user:
    def __init__(self, ID, NAME='', NICK='', TZ='US/Eastern', BOTRANK='', COLOR='', BDAY='', COUNTRY='', POINTS=0):
        self.id = ID 
        self.name = NAME
        self.tz = TZ
        self.botrank = BOTRANK
        self.nick = NICK
        self.color = COLOR
        self.bday = BDAY
        self.country = COUNTRY
        self.points = POINTS
        self.serverid = ''
        self.localrank = ''

    def decorate(self, serverid):
        self.serverid = ''
        self.nick = ''
        self.color = ''
        self.localrank = ''

        conn = sqlite3.connect(config.database)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nick, color, localrank
            FROM serverusers
            WHERE userid = ? AND serverid = ?",
            (self.id, serverid)
            )
            
        result = cursor.fetchone()
        conn.close()

        if result:
            self.serverid = serverid
            self.nick = result[0]
            self.color = result[1]
            self.localrank = result[2]
        else:
            print('No record found.')
    
    def now(self):
        return datetime.datetime.now(pytz.timezone(self.tz))
    
    def goesby(self, serverid):
        useName = ''

        if serverid != self.serverid:
            self.decorate(serverid)

        if len(self.nick) > 0:
            useName = self.nick
        else:
            useName = self.name

        return useName
            
def getUser(ID, serverid=''):
    DB = config.database

    if DB.exists():
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute(
                "SELECT name, tz, botrank, bday, country, points
                FROM users
                WHERE id = ?",
                (ID,)
                )
        result = cursor.fetchone()

        if result:
            thisUser = user(ID)
            thisUser.name = result[0]
            thisUser.tz = result[1]
            thisUser.botrank = result[2]
            thisUser.bday = result[3]
            thisUser.country = result[4]
            thisUser.points = result[5]
            
            if len(serverid) > 0:
                thisUser.decorate(serverid)

            return thisUser

        else:
            print('user not found')

def addUser(profile):
    DB = config.database
    if DB.exists():
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute(
                "INSERT INTO users(
                id, name, botrank, country, tz, bday, points)
                VALUES (?, ?, ?, ?, ?, ?, ?)",
                (profile.id, profile.name, profile.botrank,
                    profile.country, profile.tz, profile.bday, profile.points)
                )
        conn.commit()
        conn.close()

class server:
    def __init__(self, ID, NAME='', TRIGGER='!'):
        self.id = ID
        self.name = NAME
        self.trigger = TRIGGER

def getServer(serverid):
    DB = config.database
    if DB.exists():
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute(
                "SELECT name, trigger FROM servers WHERE id = ?",
                (serverid,)
                )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            thisServer = server(serverid)
            thisServer.name = result[0]
            thisServer.trigger = result[1]

            return thisServer
        
        else:
            print('Server not found!')
            
            return 0

def addServer(profile):
    DB = config.database
    if DB.exists():
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute(
                "INSERT INTO servers(
                id, name, trigger)
                VALUES (?, ?, ?)",
                (profile.id, profile.name, profile.trigger)
                )
        conn.commit()
        conn.close()
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def init():
    global databaseC
    databaseC = command('database', mSelf)
    databaseC.description = 'Commands for managing databases in the bot\'s data folder.'
    databaseC.function = 'databaseF'
    global setupC
    setupC = command('setup', databaseC)
    setupC.description = 'Initializes a new database. If the database already exists, it can be reinitialized.'
    setupC.function = 'initialize'
    global setC
    setC = command('set', databaseC)
    setC.description = 'Sets the current active database.'
    setC.function = 'setF'
    global checkC
    checkC = command('check', databaseC)
    checkC.description = 'Checks the current active database.'
    checkC.function = 'checkF'
    global listC
    listC = command('list', databaseC)
    listC.description = 'Lists all databases in the bot\'s data folder.'
    listC.function = 'listF'
    global deleteC
    deleteC = command('delete', databaseC)
    deleteC.description = 'Deletes a database. By default, deletes the currently active database if one is not specified.'
    deleteC.function = 'deleteF'
    global backupC
    backupC = command('backup', databaseC)
    backupC.description = 'Creates a backup of the selected database, or all databases.'
    backupC.function = 'backupF'
    global userC
    userC = command('user', mSelf)
    userC.description = 'Used to create, remove and manipulate user profiles.'
    userC.function = 'userF'
    global buildC
    buildC = command('build', userC)
    buildC.description = 'Builds a user object from parameters, then adds it to the database.'
    buildC.function = 'buildF'
    global timeC
    timeC = command('time', mSelf)
    timeC.description = 'Displays the current time.'
    timeC.function = 'timeF'
    global forC
    forC = command('for', timeC)
    forC.description = 'Displays the time in a specific user\'s time zone.'
    forC.function = 'timeforF'
    global zoneC
    zoneC = command('zone', timeC)
    zoneC.description = 'For configuring time zones.'
    zoneC.function = 'timezoneF'
    global listC
    listC = command('list', zoneC)
    listC.description = 'Lists all available time zones.'
    listC.function = 'timezonelistF'

def databaseF():
    print(databaseC.help() + '\n')
    listF()
    print()
    checkF()

def initialize():
    if not config.dataPath.exists():
        pathlib.path.mkdir(config.dataPath)

    DB = config.database

    try:
        doInit = False
        if DB.exists():
            response = input('Database already exists. Re-initialize? This will empty the database. <y/N> ')
            if response.lower() == 'y':
                thisDB.unlink()
                doInit = True
            else:
                print('Canceled.')
        else:
            doInit = True
        
        if doInit:
            conn = sqlite3.connect(DB)
            cursor = conn.cursor()
            cursor.execute("
                    CREATE TABLE info(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT,
                    value TEXT
                    )")
            cursor.execute("INSERT INTO info(key, value) VALUES (?, ?)",
                    ('dbversion', config.settings['dbversion']))
            print('Configuring for multiple users...')
            cursor.execute("
                    CREATE TABLE users(
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    botrank INTEGER DEFAULT '0',
                    country TEXT,
                    tz TEXT DEFAULT 'US/Eastern',
                    bday TEXT,
                    points INTEGER DEFAULT '0'
                    )")
            print('Configuring for multiple servers...')
            cursor.execute("
                    CREATE TABLE servers(
                    id TEXT NOT NULL PRIMARY KEY,
                    name TEXT,
                    trigger TEXT
                    )")
            cursor.execute("
                    CREATE TABLE serverusers(
                    userid TEXT NOT NULL,
                    serverid TEXT NOT NULL,
                    PRIMARY KEY(userid, serverid),
                    FOREIGN KEY(userid) REFERENCES users(id)
                        ON DELETE CASCADE ON UPDATE NO ACTION,
                    FOREIGN KEY(serverid) REFERENCES servers(id)
                        ON DELETE CASCADE ON UPDATE NO ACTION,
                    color TEXT,
                    nick TEXT,
                    localrank TEXT
                    )")
            conn.commit()
            conn.close()

            for module in config.imports:
                if hasattr(sys.modules[module], 'dbinit'):
                    sys.modules[module].dbinit(DB)

            print('Database initialized.')

    except:
        print(sys.exc_info()[0])
        #print('Error.')

def backup():
    timestamp = (datetime.now()).strftime("%Y%m%d%H%M%S%f")
    
    if not config.backupPath.exists():
        pathlib.path.mkdir(config.backupPath)

    backupFile = config.backupPath / ('{dbname}_backup_{code}.db'.format(dbname=config.database, code=timestamp))
    
    shutil.copy2(config.database, backupFile)

    return backupFile

def backupF():
    DB = config.database
    if DB.exists():
        oFile = backup()
        print('Database backed up to \'{backupname}\'.'.format(backupname=oFile.name))

    else:
        print('Database not found!')

def cleanup():
    backupF()

if __name__ == "__main__":
    print("No main.")
else:
    init()


>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def timeforF(userinput=''):
    if len(userinput) > 1:
        timeUser = getUser(userinput[0], userinput[1])
        print(timeUser.now())

    else:
        print('Please specify at least a user ID and a database name.')

def timezonelistF():
    for value in pytz.all_timezones:
        print(value)

#def userCF(message):
#    if len(message) > 0:
#        print(user.paramError(message))
#    else:
#        print(user.help())


def buildF(*userinput):
    newUser = user()
    userdata = []

    for p in range(0, len(userinput)):
        print(p)
        userdata.append(userinput[p].split('='))

    userDict = {}

    for q in userdata:
        userDict.update({q[0] : q[1]})

    if 'id' in userDict.keys():
        newUser.id = userDict['id']

    if 'name' in userDict.keys():
        newUser.name = userDict['name']

    if 'nick' in userDict.keys():
        newUser.nick = userDict['nick']

    if 'tz' in userDict.keys():
        newUser.tz = userDict['tz']

    if 'rank' in userDict.keys():
        newUser.rank = userDict['rank']

    if 'color' in userDict.keys():
        newUser.color = userDict['color']

    if 'bday' in userDict.keys():
        newUser.bday = userDict['bday']

    if 'country' in userDict.keys():
        newUser.country = userDict['country']

    if 'points' in userDict.keys():
        newUser.points = userDict['points']

    if 'database' in userDict.keys():
        addUser(newUser, userDict['database'])

    return newUser

def dbinit(DB):

if __name__ == "__main__":
    print("No main.")
else:
    init()