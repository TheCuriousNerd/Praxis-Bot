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

from commands.command_base import AbstractCommand

from json import loads
from urllib.parse import urlencode
import requests

import config

import bot_functions.chyron_module as chyron_module

import os
import bot_functions.praxis_logging
praxis_logger_obj = bot_functions.praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

class Command_chyron_v2(AbstractCommand, metaclass=ABCMeta):
    """
    this is the test command.
    """
    command = "!chyron"

    def __init__(self):
        super().__init__(Command_chyron_v2.command, n_args=1, command_type=AbstractCommand.CommandType.Ver2)
        self.help = ["The chyron string can be generated and updated with this command.",
        "\nExample:","chyron update \"RIGHTNOW\""]
        self.isCommandEnabled = True

    def do_command(self, source = AbstractCommand.CommandSource.default, user = "User",  command = "", rest = "", bonusData = None):
        returnString = "trying to update chyron..."
        praxis_logger_obj.log("\n [" + user + "] Command>: " + command + " " + rest)

        for name in config.adminUsers_List:
            print(name)
            tempName = user.lower()
            if name == tempName:

                try:
                    returnString = user + " has updated the chyron!"
                    chyron_ = chyron_module.Chyron_Module()

                    chyron_.main(rest)
                    chyron_.chyron_stringUpdater()
                    chyron_.updateChyronFile()
                except:
                    returnString = user + " has attempted to update the chyron but an error may have occurred!"
                #returnString = chyron_.chyron_computedString
            else:
                returnString = user + " has attempted to update the chyron but an error may have occurred further on!!!"


        return returnString

    def send_Lights_Command(self, username, light_group, command, rest):
        # todo need to url-escape command and rest
        params = urlencode({'user_name': username, 'light_group': light_group, 'command': command, 'rest':rest})
        #standalone_lights
        url = "http://standalone_lights:42042/api/v1/exec_lights?%s" % params
        resp = requests.get(url)
        if resp.status_code == 200:
            print("Got the following message: %s" % resp.text)
            data = loads(resp.text)
            msg = data['message']
            if msg is not None:
                return msg
                # todo send to logger and other relevent services
        else:
            # todo handle failed requests
            return None

    def get_help(self):
        return self.help