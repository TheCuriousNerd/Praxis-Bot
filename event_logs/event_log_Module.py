# The main repository of Praxis Bot can be found at: <https://github.com/TheCuriousNerd/Praxis-Bot>.
# Copyright (C) 2021

# Author Info Examples:
#   Name / Email / Website
#       Twitter / Twitch / Youtube / Github

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

from datetime import datetime
import random
import os
import json
import utilities_script as utility

from os import listdir
from os.path import isfile, join

class event_log():
    def __init__(self, eventName, eventTime, eventType, eventSender, eventData):
        super().__init__()
        self.eventName = eventName
        self.eventTime = eventTime
        self.eventType = eventType
        self.eventSender = eventSender
        self.eventData = eventData


class Event_Log_Module():
    def __init__(self):
        super().__init__()
        self.Event_Log_List = []
        self.Event_Log_FileName_Bonus =  "%s_%s_%s-%s_%s_%s_event_log" % (str(datetime.now().year), str(datetime.now().month), str(datetime.now().day),str(datetime.now().hour), str(datetime.now().minute), str(datetime.now().second))
        self.Event_Log_FileName = "COMPLETE_event_log"

    def main(self):
        self.load_HistoricLogs()

    def makeFile(self, fileName):
        dir = utility.get_dir("event_logs/logs")
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        relative_path = fileName + ".json"
        real_file_path = os.path.join(script_dir, dir, relative_path)

        # with open(real_file_path, 'w') as cred_w:
        #     #data = json.load(event_log_obj)
        #     dic = {}
        #     dic['eventName'] = event_log_obj.eventName
        #     dic['eventTime'] = str(event_log_obj.eventTime)
        #     dic['eventType'] = str(event_log_obj.eventType)
        #     dic['eventData'] = str(event_log_obj.eventData)
        #     json.dump(dic, cred_w, indent=2)

        newList = []
        for event in self.Event_Log_List:
            newDic = {}
            newDic['eventName'] = event.eventName
            newDic['eventTime'] = str(event.eventTime)
            newDic['eventType'] = str(event.eventType)
            newDic['eventSender'] = str(event.eventSender)
            newDic['eventData'] = str(event.eventData)
            newList.append(newDic)
        with open(real_file_path, 'w') as logFile:
            json.dump(newList, logFile, indent=2)

    def readFile(self, fileName):
        dir = utility.get_dir("event_logs/logs")
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        relative_path = fileName + ".json"
        real_file_path = os.path.join(script_dir, dir, relative_path)

        newList = []
        with open(real_file_path, 'r') as eventlog_:
            data = json.load(eventlog_)
            for d in data:
                eventName = d['eventName']
                eventTime = d['eventTime']
                eventType = d['eventType']
                eventSender = d['eventSender']
                eventData = d['eventData']

                foundLog = event_log(eventName, eventTime, eventType, eventSender, eventData)
                newList.append(foundLog)
        return newList

    def deleteFile(self, fileName):
        dir = utility.get_dir("event_logs/logs")
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        relative_path = fileName + ".json"
        real_file_path = os.path.join(script_dir, dir, relative_path)
        os.remove(real_file_path)

    def get_base_dir(self) -> str:
        cwd = os.getcwd()
        split = os.path.split(cwd)
        current = split[len(split) - 1]
        if current == 'event_logs/logs':
            return self.check_dir(cwd)
        elif current == 'Praxis-Bot' or current == 'Praxis':
            return self.check_dir(os.path.join(cwd, "event_logs/logs"))
        else:
            print("could not find working directory for Praxis-Bot/event_logs/logs")
            raise Exception

    def get_implementations_dir(self) -> str:
        return self.check_dir(os.path.join(self.get_base_dir()))

    def check_dir(self, path: str) -> str:
        if not os.path.exists(path):
            os.mkdir(path, 0x777)
        return path

    def make_event(self, eventName, eventTime, eventType, eventSender, eventData):
        newLog = event_log(eventName, eventTime, eventType, eventSender, eventData)
        self.Event_Log_List.append(newLog)
        self.makeFile(self.Event_Log_FileName)
        self.makeFile(self.Event_Log_FileName_Bonus)
        return newLog

    def get_recent_logs(self, howFarBack):
        newList = []
        try:
            for event in self.Event_Log_List:
                #recentLog = self.Event_Log_List[-x]
                newDic = {}
                newDic['eventName'] = event.eventName
                newDic['eventTime'] = str(event.eventTime)
                newDic['eventType'] = str(event.eventType)
                newDic['eventSender'] = str(event.eventSender)
                newDic['eventData'] = str(event.eventData)
                newList.append(newDic)
        except:
            return newList
        return newList

    def load_HistoricLogs(self):
        try:
            self.Event_Log_List = self.readFile(self.Event_Log_FileName)
            self.makeFile(self.Event_Log_FileName)
        except:
            pass



