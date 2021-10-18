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

from abc import ABCMeta, abstractmethod
from enum import Enum, auto

from json import loads
from urllib.parse import urlencode
import requests
from bot_functions import utilities_db as db_utility

class AbstractCommandFunction(metaclass=ABCMeta):
    class FunctionType(Enum):
        NONE = auto()
        ver0 = auto()


    def __init__(
            self,
            functionName: str,
            n_args: int = 0,
            functionType = FunctionType.NONE,
            helpText:list = ["No Help"],
            bonusFunctionData = None
        ):
        self.functionName = functionName
        self.n_args = n_args
        self.functionType = functionType #Effectively Function Version
        self.helpText = helpText
        self.bonusFunctionData = bonusFunctionData

    # no touch!
    def get_args(self, text: str) -> list:
        return text.split(" ")[0:self.n_args + 1]

    # no touch!
    def get_name(self) -> str:
        return self.functionName

    # no touch!
    def get_functionType(self):
        return self.functionType

    # no touch!
    def get_help(self):
        return self.helpText

    @abstractmethod
    def do_function(self, user, functionName, args, bonusData):
        pass

import bot_functions.praxis_logging as praxis_logging
class Function_Helpers():

    def get_Command_returnString(self, command, praxis_logger_obj:praxis_logging.praxis_logger = praxis_logging.praxis_logger()):
        try:
            db_obj = db_utility.Praxis_DB_Connection(autoConnect=True)
            returns = None
            #praxis_logger_obj.log("Getting Command ReturnString")

            query = "SELECT * FROM command_responses_v0 WHERE command = \'%s\';" % (command)
            #praxis_logger_obj.log(query)
            dbResults = db_obj.execQuery(query, praxis_logger_obj)
            #praxis_logger_obj.log("dbResults:")
            #praxis_logger_obj.log(str(dbResults))
            returns = dbResults[2]

            return returns

        except Exception as e:
            print("UNABLE TO FIND RESPONSE")
            print(e)
            return None

    def send_Lights_Command(self, username, light_group, command, rest):
        # todo need to url-escape command and rest
        params = self.urlencode({'user_name': username, 'light_group': light_group, 'command': command, 'rest':rest})
        #standalone_lights
        url = "http://standalone_lights:42042/api/v1/exec_lights?%s" % params
        resp = self.requests.get(url)
        if resp.status_code == 200:
            print("Got the following message: %s" % resp.text)
            data = self.loads(resp.text)
            msg = data['message']
            if msg is not None:
                return msg
                # todo send to logger and other relevent services
        else:
            # todo handle failed requests
            return None

    def send_TTS(self, username, message):
        params = self.urlencode({'tts_sender': username, 'tts_text': message})
        #standalone_tts_core
        url = "http://standalone_tts_core:42064/api/v1/tts/send_text?%s" % params
        resp = self.requests.get(url)
        if resp.status_code == 200:
            print("Got the following message: %s" % resp.text)
            data = self.loads(resp.text)
            msg = data['message']
            if msg is not None:
                return msg
                # todo send to logger and other relevent services
        else:
            # todo handle failed requests
            pass