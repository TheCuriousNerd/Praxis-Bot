# The main repository of Praxis_Bot can be found at: <https://github.com/TheCuriousNerd/Praxis_Bot>.
# Copyright (C) 2021

# Author Info Examples:
# Name / Email / Website
# Twitter / Twitch / Youtube

# Authors:
#   Alex Orid / inquiries@thecuriousnerd.com / TheCuriousNerd.com
#       Twitter: @TheCuriousNerd / Twitch: TheCuriousNerd / Youtube: thecuriousnerd / Github: TheCuriousNerd

# This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.

#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import json
from praxis_logging import praxis_logger
import time
import datetime
import utilities_script as utility
import importlib
import importlib.util
import sys
import inspect

class timer():
    def __init__(self,
    name,
    startTime = datetime.datetime.now,
    endTime = datetime.datetime.now,
    trigger = "",
    trigger_exec = "",
    timerFormat = "%Y-%m-%d %H:%M:%S.%f",
    tempTimer = True):
        self.name = name
        self.startTime = startTime
        self.endTime = endTime
        self.trigger = trigger
        self.trigger_exec = trigger_exec
        self.timerFormat = timerFormat
        self.tempTimer = tempTimer # If enabled this will cause the Timer to be deleted upon shutdown or startup

class Timers_Module():
    def __init__(self):
        super().__init__()
        self.timersList = {}

    def main(self):
        self.createTimer("test_timer", seconds=15)
        #self.createTimer("mega_test_timer", hours=20, seconds=10)
        #self.updateTimersList()
        #for t in self.timersList:
            #print(t)

        #while True:
            #for t in self.timersList:
            #print(t)
            #print(self.checkTimerStatus_fromFiles("test_timer"))
            #print(self.checkTimerStatus_fromFiles("test_timer_2"))
            #time.sleep(0.5)


    def updateTimersList(self):
        dic = {}
        implementations = self.get_implementations_dir()
        for dirName, subdirList, fileList in os.walk(implementations):
            for file in fileList:
                print(file)
                name, startTime, endTime, trigger, trigger_exec, timerFormat, tempTimer = self.readFile(file)
                newTimer = timer(
                    name,
                    datetime.datetime.strptime(startTime, timerFormat),
                    datetime.datetime.strptime(endTime, timerFormat),
                    trigger,
                    trigger_exec,
                    utility.strToBool(tempTimer))

                self.timersList[newTimer.name] = newTimer
        return dic


    def get_base_dir(self) -> str:
        cwd = os.getcwd()
        split = os.path.split(cwd)
        current = split[len(split) - 1]
        if current == 'timers':
            return self.check_dir(cwd)
        elif current == 'Praxis_Bot' or current == 'Praxis':
            return self.check_dir(os.path.join(cwd, "timers"))
        else:
            print("could not find working directory for Praxis_Bot/timers")
            raise Exception

    def get_implementations_dir(self) -> str:
        return self.check_dir(os.path.join(self.get_base_dir()))

    def check_dir(self, path: str) -> str:
        if not os.path.exists(path):
            os.mkdir(path, 0x777)
        return path

    def createTimer(self, name, days=0, hours=0, minutes=0, seconds=0, microseconds=0, trigger="", trigger_exec="", timerFormat='%Y-%m-%d %H:%M:%S.%f', tempTimer=True):
        startTime = datetime.datetime.now()
        targetTime = startTime + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds, microseconds=microseconds)

        newTimer= timer(name, startTime, targetTime, trigger, trigger_exec, timerFormat, tempTimer)

        self.timersList[newTimer.name] = newTimer
        self.makeFile(newTimer)

    def checkTimerStatus_fromFiles(self, name):
        try:
            if name is not None:
                name, startTime, endTime, trigger, trigger_exec, timerFormat, tempTimer = self.readFile(name+".json")
                if datetime.datetime.strptime(endTime, timerFormat) < datetime.datetime.now():
                    #print("do timer thing")
                    #self.TIMER_EXEC(name, datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f'), datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f'), trigger, trigger_exec, utility.strToBool(tempTimer))
                    return True
                else:
                    return False
            else:
                return False
        except:
            return None

    def checkTime_fromFiles(self, name):
        try:
            name, startTime, endTime, trigger, trigger_exec, timerFormat, tempTimer = self.readFile(name+".json")
            if name is not None:
                endT = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f')
                if endT.timestamp() < datetime.datetime.now().timestamp():
                    print("do timer thing")
                    endT = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f')
                    curTime = datetime.datetime.now()
                    #curTime = datetime.datetime.strptime(curTime, '%Y-%m-%d %H:%M:%S.%f')
                    result = endT - datetime.timedelta(days=curTime.day, hours=curTime.hour, minutes=curTime.minute, seconds=curTime.second, microseconds=curTime.microsecond)
                    print(type(result))

                    self.TIMER_EXEC(name, datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f'), datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f'), trigger, trigger_exec, utility.strToBool(tempTimer))
                    fixedEndTime = datetime.datetime.strftime(result, timerFormat)
                    return str("Timer Done")
                else:
                    endT = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f')
                    curTime = str(datetime.datetime.now())
                    curTime = datetime.datetime.strptime(curTime, '%Y-%m-%d %H:%M:%S.%f')
                    result = endT - datetime.timedelta(days=curTime.day, hours=curTime.hour, minutes=curTime.minute, seconds=curTime.second, microseconds=curTime.microsecond)

                    fixedEndTime = datetime.datetime.strftime(result, timerFormat)
                    #fixedTimeDelta = fixedEndTime - fixedCurTime
                    #praxis_logger.log(str(timeDelta))
                    return str(fixedEndTime)
            else:
                return None
        except:
            return None

    def deleteTimer(self, name):
        try:
            self.deleteFile(name+".json")
        except:
            print("Deletion Error")
        self.timersList.pop(name)


    def TIMER_EXEC(self, name, startTime, endTime, trigger, trigger_exec, tempTimer):
        print(trigger, trigger_exec, "at", endTime)

        if tempTimer == True:
            print("deleting " + name)
            self.deleteTimer(name)


    def makeFile(self, timer_obj:timer):
        dir = utility.get_dir("timers")
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        relative_path = timer_obj.name + ".json"
        real_file_path = os.path.join(script_dir, dir, relative_path)

        with open(real_file_path, 'w') as cred_w:
            #data = json.load(timer_obj)
            dic = {}
            dic['name'] = timer_obj.name
            dic['startTime'] = str(timer_obj.startTime)
            dic['endTime'] = str(timer_obj.endTime)
            dic['trigger'] = timer_obj.trigger
            dic['trigger_exec'] = timer_obj.trigger_exec
            dic['timerFormat'] = timer_obj.timerFormat
            dic['tempTimer'] = str(timer_obj.tempTimer)
            json.dump(dic, cred_w, indent=2)


    def readFile(self, name):
        dir = utility.get_dir("timers")
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        relative_path = name #+ ".json"
        real_file_path = os.path.join(script_dir, dir, relative_path)

        with open(real_file_path, 'r') as cred_r:
            data = json.load(cred_r)
            name = data['name']
            startTime = data['startTime']
            endTime = data['endTime']
            trigger = data['trigger']
            trigger_exec = data['trigger_exec']
            timerFormat = data['timerFormat']
            tempTimer = data['tempTimer']
        return name, startTime, endTime, trigger, trigger_exec, timerFormat, tempTimer

    def deleteFile(self, name):
        dir = utility.get_dir("timers")
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        relative_path = name #+ ".json"
        real_file_path = os.path.join(script_dir, dir, relative_path)
        os.remove(real_file_path)


if __name__ == "__main__":
    testModule = Timers_Module()
    testModule.main()
