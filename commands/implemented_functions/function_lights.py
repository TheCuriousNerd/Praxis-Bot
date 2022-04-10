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
from ast import arg

from json import loads
from urllib.parse import urlencode
import requests

from commands.command_base import AbstractCommand
from commands.command_functions import AbstractCommandFunction

from commands.command_functions import Abstract_Function_Helpers

from bot_functions import utilities_script as utility

import config

class Function_Lights(AbstractCommandFunction, metaclass=ABCMeta):
    """
    This is v0 of Functions
    """
    functionName = "lights"
    warningText = []
    helpText = ["This will change the state of the lights in the specified group.",
        "\nExample:","($lights (group)(command))"]

    def __init__(self):
        super().__init__(
            functionName = Function_Lights.functionName,
            n_args = 0,
            functionType = AbstractCommandFunction.FunctionType.ver0,
            helpText = Function_Lights.helpText,
            bonusFunctionData = None
            )

    def do_function(self, tokenSource, user, functionName, args, bonusData):
        output = self.do_work(user, functionName, args, bonusData)

        return output

    def do_work(self, user, functionName, args, bonusData):

        try:
            lightGroup = args[0]
            lightCommandList = args
            lightCommandList.pop(0)
            lightCommand = " ".join(lightCommandList)

            # todo need to url-escape command and rest
            params = urlencode({'user_name': user["userName"], 'light_group': lightGroup, 'command': lightCommand, 'rest':""})

            url = "http://%s:%s/api/v1/exec_lights?%s" % (config.standalone_lights_address[0].get("ip"), config.standalone_lights_address[0].get("port"), params)
            #url = "http://%s:%s/api/v1/exec_lights?%s" % ("127.0.0.1", config.standalone_lights_address[0].get("port"), params)
            #standalone-lights
            # if utility.isRunningInDocker():
            #     url = "http://%s:%s/api/v1/exec_lights?%s" % (config.standalone_lights_address[0].get("ip"), config.standalone_lights_address[0].get("port"), params)
            # else:
            #     url = "http://%s:%s/api/v1/exec_lights?%s" % ("127.0.0.1", config.standalone_lights_address[0].get("port"), params)
            resp = requests.get(url)
            if resp.status_code == 200:
                print("Got the following message: %s" % resp.text)
                data = loads(resp.text)
                msg = data['message']
                if msg is not None:
                    return ""
                    # todo send to logger and other relevent services
            else:
                # todo handle failed requests
                return "Something went wrong"
        except Exception as e:
            # todo handle exceptions
            return str(e)

        return ""
