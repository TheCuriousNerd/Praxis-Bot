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


from abc import ABCMeta

from json import loads
from urllib.parse import urlencode
import requests

from commands.command_base import AbstractCommand
from commands.command_functions import AbstractCommandFunction, Function_Helpers

from bot_functions import utilities_script as utility
from bot_functions import token_processor

import pyparsing

class Command_v3(AbstractCommand, AbstractCommandFunction, metaclass=ABCMeta):
    """
    this is the v3 command.
    """
    command = "base_v3"
    helpText = ["This is the v3 command.",
        "\nExample:","base_v3","base_v3 ARGZ"]

    def __init__(self):
        super().__init__(
            Command_v3.command,
            n_args=1,
            command_type=AbstractCommand.CommandType.Ver3
            )
        self.helpText = Command_v3.helpText
        self.isCommandEnabled = True

    def do_command(self, source = AbstractCommand.CommandSource.default, user = "User",  command = "", rest = "", bonusData = None):

        # Command Example:
        # Idea: "!roll #(0)" = "!roll d20"
        # command = "!roll"
        # rest = " #(0)" = " d20"

        # Look up command in DB and get return strings.
        commandName = command
        v3helper = Function_Helpers()
        v3cmd_response = v3helper.get_Command_returnString(commandName)
        #if v3cmd_response is None:
        #    return "not none"
        enoughArgs = self.enoughArgs(rest, v3cmd_response)

        # Proccess strings
        commandRawInput = commandName + " " + rest # This creates the full command string.
        # Gets rid of the empty space if there are no arguments provided by the user
        if rest is "":
            commandRawInput = commandRawInput [:-1]
        if not enoughArgs:
            return "Not enough arguments, try again!"

        tokenWorker = token_processor.Token_Processor()
        tokenWorker.loadedFunctions = self.loadedFunctions
        tokenWorker_Results = tokenWorker.parseTokenResponse(user, commandRawInput, v3cmd_response)
        returnString = tokenWorker_Results

        return returnString

    def enoughArgs(self, args, v3cmd_response):
        howManyArgsNeeded = 0
        howManyArgsAvailable = 0
        argRange = range(25)
        for i in argRange:
            if ("$(#%s)" % str(i)) in v3cmd_response:
                howManyArgsNeeded = howManyArgsNeeded + 1

        args = utility.get_args(args)
        for a in args:
            if a is not "":
                howManyArgsAvailable = howManyArgsAvailable + 1

        if howManyArgsAvailable >= howManyArgsNeeded:
            return True
        else:
            return False


    def get_help(self):
        return self.helpText

    def do_function():
        return None