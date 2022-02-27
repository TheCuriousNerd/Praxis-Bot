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

from json import dumps, loads
from urllib.parse import urlencode
from urllib.parse import parse_qs
import requests
import re

import config

import bot_functions.utilities_db as utilities_db
import time

import os
import bot_functions.praxis_logging as praxis_logging
praxis_logger_obj = praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

class Command_tts_v2(AbstractCommand, metaclass=ABCMeta):
    """
    this is the tts command.
    """
    command = "!tts"

    def __init__(self):
        super().__init__(Command_tts_v2.command, n_args=1, command_type=AbstractCommand.CommandType.Ver2)
        self.help = ["This command allows you to do tts.",
        "\nExample:","tts \"TEXT\""]
        self.isCommandEnabled = True

    def do_command(self, source = AbstractCommand.CommandSource.default, user:str = "User", userID = "0",  command = "", rest = "", bonusData = None):
        returnString = user + " sent a tts command!"
        praxis_logger_obj.log("\n Command>: " + command + rest)


        if "Twitch" in source:
            for name in config.allowedTTS_List:
                print(name)
                tempName = user.lower()
                if name == tempName:
                    self.send_TTS(user, rest)
                    db = utilities_db.Praxis_DB_Connection(autoConnect=True)
                    db.add_taskToQueue("standalone_discord", "voice", str(time.time()), "play", dumps({"type":"tts","text":rest}), "")
        elif "Discord" in source:
            for name in config.allowedTTS_List:
                print(name)

                tempNick = self.contains_value("(?<=nick=')[^']+", bonusData)

                tempName = user.lower()
                if name == str(userID):
                    self.send_TTS(tempNick, rest)

                    db = utilities_db.Praxis_DB_Connection(autoConnect=True)
                    db.add_taskToQueue("standalone_discord", "voice", str(time.time()), "play", dumps({"type":"tts","text":rest}), "")
        else:
            returnString = self.send_TTS(user, rest)



        #for name in config.allowedCommandsList_TwitchPowerUsers:
            #print(name)
            #tempName = user.lower()
            #if name == tempName:
                #self.send_TTS(user, rest)

        return returnString

    def send_Lights_Command(self, username, light_group, command, rest):
        # todo need to url-escape command and rest
        params = urlencode({'user_name': username, 'light_group': light_group, 'command': command, 'rest':rest})
        #standalone_lights
        url = "http://%s:%s/api/v1/exec_lights?%s" % (config.standalone_lights_address[0].get("ip"), config.standalone_lights_address[0].get("port"), params)
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
            pass

    def send_TTS(self, username, message):
        params = urlencode({'tts_sender': username, 'tts_text': message})
        #standalone_tts_core
        url = "http://%s:%s/api/v1/tts/send_text?%s" % (config.standalone_tts_core_address[0].get("ip"), config.standalone_tts_core_address[0].get("port"), params)
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
            pass

    def contains_value(self, search: str, data:str):
        contains = re.search(search, data)
        return contains.group(0)

    def get_help(self):
        return self.help