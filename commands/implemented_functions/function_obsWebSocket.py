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
import json

class Function_obsWebSocket(AbstractCommandFunction, metaclass=ABCMeta):
    """
    This is v0 of Functions
    """
    functionName = "obsWebSocket"
    warningText = []
    helpText = ["This will send a request to the OBS WebSocket.",
        "\nExample:","($obsWebSocket (requestType)(data))"]

    def __init__(self):
        super().__init__(
            functionName = Function_obsWebSocket.functionName,
            n_args = 0,
            functionType = AbstractCommandFunction.FunctionType.ver0,
            helpText = Function_obsWebSocket.helpText,
            bonusFunctionData = None
            )

    def do_function(self, tokenSource, user, functionName, args, bonusData):
        output = self.do_work(user, functionName, args, bonusData)

        return output

    def do_work(self, user, functionName, args, bonusData):
        print(args)
        # newData:list = args
        # newData.pop(0)
        # newData = " ".join(newData)
        # newDataDict = json.loads(newData)
        #return str(type(return_stuff))
        try:
            from bot_functions import obsWebSocket as obsWebSocket

            newData:list = args
            requestType = newData.pop(0)
            newData = " ".join(newData)
            newDataDict = json.loads(newData)
            output = obsWebSocket.makeRequest(requestType, newDataDict)
            print(output)
            return ""
        except Exception as e:
            #return "[obs websocket error][Error: %s]" % e
            return "[obs websocket error]"
