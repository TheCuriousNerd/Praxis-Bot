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
from distutils.command.config import config

from json import loads
from urllib.parse import urlencode
import requests

from commands.command_base import AbstractCommand
from commands.command_functions import AbstractCommandFunction

from commands.command_functions import Abstract_Function_Helpers

from bot_functions import utilities_script as utility
from bot_functions import utilities_db

import config as praxis_config

class Function_ChyronRefresh(AbstractCommandFunction, metaclass=ABCMeta):
    """
    This is v0 of Functions
    """
    functionName = "refreshChyron"
    warningText = []
    helpText = ["This function will refresh the chyron file on the server.",
        "\nExample:","($refreshChyron)"]

    def __init__(self):
        super().__init__(
            functionName = Function_ChyronRefresh.functionName,
            n_args = 0,
            functionType = AbstractCommandFunction.FunctionType.ver0,
            helpText = Function_ChyronRefresh.helpText,
            bonusFunctionData = None
            )

    def do_function(self, tokenSource, user, functionName, args, bonusData):
        output = self.do_work(user, functionName, args, bonusData)

        return output

    def do_work(self, user, functionName, args, bonusData):
        tableName = "home_praxisbot_chyron_entry"

        try:
            targetVar = args[0]
            newData = args
            newData.pop(0)
            newData = " ".join(newData)

            db = utilities_db.Praxis_DB_Connection(autoConnect=True)

            if db.doesItemExist(tableName, "tag", targetVar):
                url="http://%s:%s/api/v1/chyron/update_file" % (praxis_config.standalone_command_address[0].get("ip"), praxis_config.standalone_command_address[0].get("port"))
                resp = requests.get(url)
        except:
            return "[Error refreshing Chyron]"

        return ""