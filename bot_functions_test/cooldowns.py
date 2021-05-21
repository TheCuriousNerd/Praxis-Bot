# The main repository of Praxis Bot can be found at: <https://github.com/TheCuriousNerd/Praxis-Bot>.
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

import random
import re

import datetime
from datetime import timedelta

import time
from time import sleep

class Cooldown_Action:
    def __init__(self):
        self.tag:str = ""
        self.time = datetime.datetime.now()

class Cooldown:
    def __init__(self):
        self.cooldownName:str = ""
        self.cooldownActionLimit:int = 0
        self.cooldownDuration:int = 0 #Seconds

        self.actionList:list = []

    def setupCooldown(self, name, limit, duration):
        self.cooldownName = name
        self.cooldownActionLimit = limit
        self.cooldownDuration = duration

class Cooldown_Module:
    def __init__(self):
        super().__init__()
        self.cooldownList:list = []

    def setupCooldown(self, name, limit, duration):
        newCD:Cooldown = Cooldown()
        newCD.setupCooldown(name, limit, duration)
        self.cooldownList.append(newCD)


    def getCooldown(self, name:str):
        returnCD:bool = False
        for cd in self.cooldownList:
            if cd.cooldownName == name:
                returnCD = True
                return cd
        if returnCD == False:
            return None

    def isCooldownActive(self, name:str):
        isCooldownActivated:bool = False

        selectedCooldown:Cooldown = self.getCooldown(name)

        if selectedCooldown == None:
            return None

        timenow = datetime.datetime.now()

        if len(selectedCooldown.actionList) >= selectedCooldown.cooldownActionLimit:
            actionCount = len(selectedCooldown.actionList)

            maxTmpIndex = actionCount - selectedCooldown.cooldownActionLimit
            maxRecentAction:Cooldown_Action = selectedCooldown.actionList[maxTmpIndex]

            timeDiff = timenow - maxRecentAction.time
            maxTimeAllowed = timedelta(seconds = selectedCooldown.cooldownDuration)

            if timeDiff < maxTimeAllowed:
                isCooldownActivated = True

        return isCooldownActivated

    def actionTrigger(self, name:str = "", tag:str = ""):
        newAction = Cooldown_Action()
        newAction.tag = tag
        targetCD = self.getCooldown(name)
        if targetCD != None:
            targetCD.actionList.append(newAction)

if __name__ == "__main__":
    testCD = Cooldown_Module()
    cdName = "test"
    testCD.setupCooldown(cdName, 20, 2)

    print("CD Test 0: ")
    for x in range(20):
        testCD.actionTrigger("cdName")
        sleep(0)
    print(testCD.isCooldownActive("cdName"))
    print("//Test Done//")
    sleep(2)

    print("CD Test 1: ")
    for x in range(20):
        testCD.actionTrigger(cdName)
        sleep(0)
    print(testCD.isCooldownActive("test"))
    print("//Test Done//")
    sleep(2)

    print("CD Test 2: ")
    for x in range(10):
        testCD.actionTrigger(cdName)
        sleep(0)
    print(testCD.isCooldownActive(cdName))
    print("//Test Done//")
    sleep(2)

    print("CD Test 3: ")
    for x in range(20):
        testCD.actionTrigger(cdName)
        sleep(0.05)
    print(testCD.isCooldownActive(cdName))
    print("//Test Done//")
    sleep(2)

    print("CD Test 4: ")
    for x in range(20):
        testCD.actionTrigger(cdName)
        sleep(0.6)
    print(testCD.isCooldownActive(cdName))
    print("//Test Done//")