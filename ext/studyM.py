import sys
import sqlite3
from datetime import *

from core import config
from core.commandM import command
from core import DBM

mSelf = sys.modules[__name__]
includes = {}
config.imports.append(__name__)

class studyUser(DBM.user):
    def __init__(self, ID, CSTREAK=None, LSTREAK=None, DAYS=None):
        self.cstreak = CSTREAK
        self.lstreak = LSTREAK
        self.days = DAYS

        tempUser = DBM.tryGetOneUser(ID)
        if tempUser:
            super().__init__(tempUser.id, tempUser.name, tempUser.tz, tempUser.botrank, tempUser.bday, tempUser.country, tempUser.points)
        else:
            super().__init__(ID)

def getStudyUser(userid):
    DB = config.database

    thisUser = DBM.getUser(userid)

    if thisUser:
        if DBM.checkDB():
            conn = sqlite3.connect(DB)
            cursor = conn.cursor()
            cursor.execute(
                    "SELECT cstreak, lstreak, days "
                    "FROM studyusers "
                    "WHERE user = ?",
                    (userid,)
                    )
            result = cursor.fetchone()
            conn.close()

            if result:
                thisStudyUser = studyUser(thisUser.id)
                thisStudyUser.cstreak = result[0]
                thisStudyUser.lstreak = result[1]
                thisStudyUser.days = result[2]

                return thisStudyUser

            else:
                return None

    else:
        return None

def tryGetOneStudyUser(studyuserstring):
    thisStudyUser = None

    try:
        thisStudyUser = getStudyUser(int(studyuserstring))

    except ValueError:
        thisUser = DBM.tryGetOneUser(studyuserstring)

        if thisUser:
            thisStudyUser = getStudyUser(thisUser.id)

    return thisStudyUser

def addStudyUser(profile):
    DB = config.database

    if DBM.checkDB():
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute(
                "INSERT INTO studyusers"
                "(user, cstreak, lstreak, days) "
                "VALUES (?, ?, ?, ?)",
                (profile.id, profile.cstreak, profile.lstreak, profile.days)
                )
        conn.commit()
        conn.close()

def removeStudyUser(profile):
    DB = config.database

    if DBM.checkDB():
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute(
                "DELETE FROM studyusers "
                "WHERE user = ?",
                (profile.id,)
                )
        conn.commit()
        conn.close()

def updateStudyUser(profile):
    thisStudyUser = getStudyUser(profile.id)

    if thisStudyUser:
        if profile.cstreak:
            thisStudyUser.cstreak = profile.cstreak
        if profile.lstreak:
            thisStudyUser.lstreak = profile.lstreak
        if profile.days:
            thisStudyUser.days = profile.days

        DB = config.database

        if DBM.checkDB():
            conn = sqlite3.connect(DB)
            cursor = conn.cursor()
            cursor.execute(
                    "UPDATE studyusers SET "
                    "cstreak = ?, lstreak = ?, days = ? "
                    "WHERE user = ?",
                    (thisStudyUser.cstreak, thisStudyUser.lstreak, thisStudyUser.days, thisStudyUser.id)
                    )
            conn.commit()
            conn.close()

def searchStudyUserbyName(searchstring):
    search = DBM.searchUserbyName(searchstring)

    if search:
        foundStudyUsers = []

        for result in search:
            thisStudyUser = getStudyUser(result.id)

            if thisStudyUser:
                foundStudyUsers.append(thisStudyUser)

        if len(foundStudyUsers) > 0:
            return foundStudyUsers

        else:
            return None

    else:
        return None

def searchStudyUserbyServer(serverprofile):
    search = DBM.searchUserbyServer(serverprofile)

    if search:
        foundStudyUsers = []
        
        for result in search:
            thisStudyUser = getStudyUser(result.id)

            if thisStudyUser:
                foundStudyUsers.append(thisStudyUser)

        if len(foundStudyUsers) > 0:
            return foundStudyUsers

        else:
            return None

    else:
        return None
        
class studyLog:
    def __init__(self, ID=None, USER=None, DATE=None, NOTE=None):
        self.id = ID
        self.user = USER
        self.date = DATE
        self.note = NOTE

def getStudyLog(logid):
    DB = config.database

    if DBM.checkDB():
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute(
                "SELECT user, date, note "
                "FROM studysessions "
                "WHERE id = ?",
                (logid,)
                )
        result = cursor.fetchone()
        conn.close()

        if result:
            thisStudyLog = studyLog(logid)
            thisStudyLog.user = result[0]
            thisStudyLog.date = result[1]
            thisStudyLog.note = result[2]

            return thisStudyLog

        else:
            return None

def addStudyLog(profile):
    DB = config.database

    if DBM.checkDB():
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute(
                "INSERT INTO studysessions"
                "(user, date, note) "
                "VALUES (?, ?, ?)",
                (profile.user, profile.date, profile.note)
                )
        conn.commit()
        conn.close()

def removeStudyLog(profile):
    DB = config.database

    if DBM.checkDB():
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute(
                "DELETE FROM studysessions "
                "WHERE id = ?",
                (profile.id,)
                )
        conn.commit()
        conn.close()

def updateStudyLog(profile):
    thisStudyLog = getStudyLog(profile.id)

    if thisStudyLog:
        if profile.user:
            thisStudyLog.user = profile.user
        if profile.date:
            thisStudyLog.date = profile.date
        if profile.note:
            thisStudyLog.note = profile.note

        DB = config.database

        if DBM.checkDB():
            conn = sqlite3.connect(DB)
            cursor = conn.cursor()
            cursor.execute(
                    "UPDATE studysessions SET "
                    "user = ?, date = ?, note = ? "
                    "WHERE id = ?",
                    (thisStudyLog.user, thisStudyLog.date, thisStudyLog.note, thisStudyLog.id)
                    )
            conn.commit()
            conn.close()

def searchStudyLogbyUser(profile):
    DB = config.database
    if DBM.checkDB():
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute(
                "SELECT id "
                "FROM studysessions "
                "WHERE user = ?",
                (profile.id,)
                )
        search = cursor.fetchall()
        conn.close()

        if len(search) > 0:
            foundStudyLogs = []
            for result in search:
                thisStudyLog = getStudyLog(result[0])
                foundStudyLogs.append(thisStudyLog)

            return foundStudyLogs

        else:
            return None

def init():
    global studyC
    studyC = command('study', mSelf)
    studyC.description = 'Commands for tracking and monitoring study habits.'
    studyC.function = 'studyF'
    global logC
    logC = command('log', studyC)
    logC.description = 'For managing tracked study sessions.'
    logC.function = 'logF'
    global markC 
    markC= command('mark', logC)
    markC.description = 'Marks you as having studied for the day.'
    markC.function = 'markF'
    global unmarkC
    unmarkC = command('unmark', logC)
    unmarkC.description = 'Unmarks you as having studied for the day.'
    unmarkC.function = 'unmarkF'
    global checkC
    checkC = command('check', logC)
    checkC.description = 'Returns whether study has been logged for the current day.'
    checkC.function = 'checkF'

def logF():
    print(logC.help())

def studyF():
    print(studyC.help())

def markF(userinput):
    userString = userinput[0]
    logNote = ' '.join(userinput[1:])

    thisUser = DBM.tryGetOneUser(userString)

    if thisUser:
        logDate = DBM.getTime(thisUser).strftime("%d-%m-%Y")
        print(logDate)

        thisLog = studyLog()
        thisLog.user = thisUser.id
        thisLog.date = logDate
        thisLog.note = logNote

        addStudyLog(thisLog)

        print('Study logged for {uname} on {ldate}.'.format(uname=thisUser.name, ldate=logDate))

    else:
        print('User not found.')
        
def unmarkF(userinput):
    userString = userinput[0]
    thisUser = DBM.tryGetOneUser(userString)

    if thisUser:
        search = searchStudyLogbyUser(thisUser)

        if search:
            if len(userinput) > 1:
                dateString = ' '.join(userinput[1:])

            else:
                dateString = DBM.getTime(thisUser).strftime("%d-%m-%Y")

            foundLog = None

            for result in search:
                if result.date == dateString:
                    foundLog = result

            if foundLog:
                removeStudyLog(foundLog)
                print('{uname} unmarked for {ldate}.'.format(uname=thisUser.name, ldate=foundLog.date))

            else:
                print('{uname} did not study on {ldate}.'.format(uname=thisUser.name, ldate=dateString))

        else:
            print('No logs found.')

    else:
        print('User not found.')

def checkF(userinput):
    userString = userinput[0]

    thisUser = DBM.tryGetOneUser(userString)

    if thisUser:
        search = searchStudyLogbyUser(thisUser)

        if search:
            if len(userinput) > 1:
                dateString = ' '.join(userinput[1:])

            else:
                dateString = DBM.getTime(thisUser).strftime("%d-%m-%Y")

            foundLog = None

            for result in search:
                if result.date == dateString:
                    foundLog = result

            if foundLog:
                if foundLog.note:
                    print('{uname} studied on {ldate}.\n"{lnote}"'.format(uname=thisUser.name, ldate=foundLog.date, lnote=foundLog.note))
                else:
                    print('{uname} studied on {ldate}.'.format(uname=thisUser.name, ldate=foundLog.date))

            else:
                print('{uname} did not study on {ldate}.'.format(uname=thisUser.name, ldate=dateString))

        else:
            print('No logs found.')

    else:
        print('User not found.')

def dbinit(DB):
    print('Configuring for study logging...')
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
            "CREATE TABLE studysessions("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, user INTEGER, date TEXT, note TEXT, "
            "FOREIGN KEY(user) REFERENCES users(id) ON DELETE CASCADE ON UPDATE NO ACTION)"
            )
    cursor.execute(
            "CREATE TABLE studyusers("
            "user INTEGER PRIMARY KEY, cstreak INTEGER DEFAULT 0, lstreak INTEGER DEFAULT 0, days INTEGER DEFAULT 0, "
            "FOREIGN KEY(user) REFERENCES users(id) ON DELETE CASCADE ON UPDATE NO ACTION)"
            )
    conn.commit()
    conn.close()

def cleanup():
    print('study cleanup...')

if __name__ == "__main__":
    print('A collection of study tracking commands for a botParts bot. No main.')
else:
    init()
