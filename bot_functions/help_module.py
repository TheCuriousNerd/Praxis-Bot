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

from commands.command_base import AbstractCommand
from enum import Enum
import config as config

from commands import loader as command_loader

import credentials

class Help_Module():
    def __init__(self):
        super().__init__()

    def main(self):
        print("[Help Module]> help test")
        self.isCommandEnabled = True

    def help_command_response(self, command:AbstractCommand, responseType):
        response = help_command_response()
        response.setup(command, responseType)
        response.makeResponse()
        return response

class help_command_responseType(Enum):
    plain = 1 # One line response
    fancy = 2 # Fancy formatted response

class help_command_response():
    def __init__(self):
        super().__init__()
        self.command = None
        self.commandName = ""
        self.helpText = ""
        self.response = ""
        self.responseType = help_command_responseType.plain
        self.blockDecor = "\n================================================================\n"

    def setup(self, command, responseType):
        self.command = command
        self.commandName = command.command
        self.responseType = responseType

    def makeResponse(self):
        if self.responseType == help_command_responseType.plain:
            self.response_plain()
        elif self.responseType == help_command_responseType.fancy:
            self.response_fancy()

    def response_plain(self):
        tempHelpText = ""
        for line in self.command.help:
            tempHelpText = tempHelpText + line + " "
        self.response = "Command: " + self.commandName + " : " + self.helpText
        return self.response

    def response_fancy(self):
        tempHelpText = ""
        for line in self.command.help:
            tempHelpText = tempHelpText + line + "\n"
        self.response = self.blockDecor + "Command: " + self.commandName + self.blockDecor + tempHelpText + self.blockDecor
        return self.response



Help_Module_ = Help_Module()

if __name__ == "__main__":
    testModule = Help_Module()

    testModule.main()