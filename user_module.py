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

from enum import Enum
import time
import config as config
from bot_functions import tts as tts

import credentials

from commands import loader as command_loader
from commands.command_base import AbstractCommand

from bot_functions.cooldowns import Cooldown_Module

from bot_functions import utilities_script as utility

class User_Module():
    def __init__(self):
        super().__init__()
        self.MessageLog:list = []
        self.commands = command_loader.load_commands_new(AbstractCommand.CommandType.Praxis)
        self.UseFlagTypeMap = {  # this is a mapping of the UserFlagTypes enum to function pointers
            UserFlagTypes.REACTIVE: self.eval_commands_Special_Reactive}

        self.currentUser:User = User()
        self.inputLoop = True

    def main(self):
        time.sleep(.01)
        print("\nWaiting on User input...\n\n")
        if utility.isRunningInDocker() == True:
            self.inputLoop = False
            print("\nNo User's Input Allowed")

        while self.inputLoop:
            keyboardInput = input()
            message = UserMessage()
            message.makeMessage(self.currentUser, keyboardInput)

            self.parseInput(message)

    def parseInput(self, message):
        if self.isCommand(message) == True:
            self.runCommand(message)
        else:
            pass

    def isCommand(self, message):
        isCommand = True
        #MAKE THIS
        return isCommand

    def runCommand(self, message):
        if not self.eval_commands_SpecialActionCheck():
            self.eval_commands(message)

    def eval_commands(self, message):
        # containsURL: bool = self.contains_url(message)
        try:
            #first_space_idx = message.text.index(' ')

            # This fixes a error where if you send a command without arguments it fails because
            # it cant find the substring.
            if message.message.find(" ") != -1:
                first_space_idx = message.message.index(' ')
            else:
                first_space_idx = -1

            command_text = ' '
            if first_space_idx > -1:
                command_text = message.message[0:first_space_idx]
            else:
                command_text = message.message

            command = self.commands[command_text]
            if command is not None and command.command_type is AbstractCommand.CommandType.Praxis:
                command.do_command(self, message)
        except Exception as e:
            # Undo the following for debug stuff
            #print(e)
            pass  # we don't care

    def eval_commands_SpecialActionCheck(self):
        foundSomething = False
        return foundSomething

    def eval_commands_Special_Reactive(self):
        pass

    def return_message(self, returnedMessage):
        print(returnedMessage)

    def tts(self, message):
        tts.tts(message)

class User():
    def __init__(self, username:str = "User"):
        super().__init__()
        self.name = username
        self.flags = {}

    def setFlag(self, name, flagType):
        flag:UserFlag = UserFlag(name, flagType)
        self.flags[name] = flag

    def getFlag(self, name):
        return self.flags[name]

    def deleteFlag(self, name):
        return self.flags.pop(name, None)

class UserMessage():
    def __init__(self, user = User(), message = ""):
        super().__init__()
        self.user = user
        self.message:str = message

    def makeMessage(self, user = "User", message = ""):
        self.user = user
        self.message = message

class UserFlagTypes(Enum):
    REACTIVE = 1

class UserFlag():
    def __init__(self, flagName = "User", flagType:UserFlagTypes = None):
        super().__init__()
        self.name = flagName
        self.flagType:UserFlagTypes = flagType



if __name__ == "__main__":
    testModule = User_Module()

    testModule.main()