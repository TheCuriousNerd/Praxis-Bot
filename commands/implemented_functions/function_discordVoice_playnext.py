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

from json import dump, loads
from time import time
from urllib.parse import urlencode
import requests

import time

from commands.command_base import AbstractCommand
from commands.command_functions import AbstractCommandFunction

from commands.command_functions import Abstract_Function_Helpers

from bot_functions import utilities_script as utility
from bot_functions import utilities_db

import datetime

class Function_discordVoice_playnext(AbstractCommandFunction, metaclass=ABCMeta):
    """
    This is v0 of Functions
    """
    functionName = "discordVoicePlayNext"
    warningText = ["CAUTION: This function is not yet implemented."]
    helpText = ["This will cause the bot to play a file or text to the voice channel after the current one is finished.",
        "\nExample:","($discordVoicePlayNext (Thing to play next))"]

    def __init__(self):
        super().__init__(
            functionName = Function_discordVoice_playnext.functionName,
            n_args = 0,
            functionType = AbstractCommandFunction.FunctionType.ver0,
            helpText = Function_discordVoice_playnext.helpText,
            bonusFunctionData = None
            )

    def do_function(self, tokenSource, user, functionName, args, bonusData):
        output = ""
        if tokenSource is AbstractCommand.CommandSource.Discord:
            output = self.do_work(user, functionName, args, bonusData)
        else:
            output = "[Unable to use function in this context]"

        return output

    def do_work(self, user, functionName, args, bonusData):
        inputArgs = utility.list_to_string(args)
        newAudio = {}
        # Determine if inputArgs is either a url, a file, or a string
        if utility.contains_url(inputArgs):
            # inputArgs is a url
            newAudio["type"] = "url"
        elif utility.contains_pattern(inputArgs, ".*\.(mp3|pcm|wav|aiff|aac|ogg|wma|flac|alac)$"):
            # inputArgs is a file
            newAudio["type"] = "file"
        else:
            # inputArgs is a string
            newAudio["type"] = "tts"
        newAudio["text"] = inputArgs
        preppedAudio = dump(newAudio)

        db = utilities_db.Praxis_DB_Connection(autoConnect=True)
        db.add_taskToQueue("standalone_discord", "voice", str(time.time()), "playNext", preppedAudio, "")
        return args

