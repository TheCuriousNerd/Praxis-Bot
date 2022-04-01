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

class Function_discordVoice_discordName(AbstractCommandFunction, metaclass=ABCMeta):
    """
    This is v0 of Functions
    """
    functionName = "discordName"
    warningText = ["This function is not yet implemented."]
    helpText = ["This will fetch the discord name of a user",
        "\nExample:","($discordName (TheCuriousNerd))"
        "\nExample:","($discordName (Discord ID Here))"]

    def __init__(self):
        super().__init__(
            functionName = Function_discordVoice_discordName.functionName,
            n_args = 0,
            functionType = AbstractCommandFunction.FunctionType.ver0,
            helpText = Function_discordVoice_discordName.helpText,
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
        db = utilities_db.Praxis_DB_Connection(autoConnect=True)
        db.add_taskToQueue("standalone_discord", "user", str(time.time()), "name", user, "")

        # Sleep for a bit and then check to see if the task is done
        sleepy = True
        while sleepy:
            db_data = db.getTasksFromQueue("standalone_function")
            if db_data[5] == user:
                userName = db_data[6]
                sleepy = False
                db_data = db.deleteItems("task_queue_v0", "id", db_data[0])
            else:
                time.sleep(1)

        return userName

