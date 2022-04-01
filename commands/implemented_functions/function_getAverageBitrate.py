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

import simpleobsws
import config

class Function_GetBitrate(AbstractCommandFunction, metaclass=ABCMeta):
    """
    This is v0 of Functions
    """
    functionName = "getAverageBitrate"
    warningText = []
    helpText = ["This will return the average bitrate of the stream.",
        "NOTE: This is not the bitrate of the stream, but the average bitrate of the stream.",
        "This is calculated by the total bytes sent over the last 30 seconds, divided by the total duration of the stream in seconds.",
        "OBS currently does not provide the actual current bitrate of the stream, so this is a best guess.",
        "\nExample:","($getAverageBitrate)"]

    def __init__(self):
        super().__init__(
            functionName = Function_GetBitrate.functionName,
            n_args = 0,
            functionType = AbstractCommandFunction.FunctionType.ver0,
            helpText = Function_GetBitrate.helpText,
            bonusFunctionData = None
            )

    def do_function(self, tokenSource, user, functionName, args, bonusData):
        output = self.do_work(user, functionName, args, bonusData)

        return output

    def do_work(self, user, functionName, args, bonusData):

        try:
            from bot_functions import obsWebSocket as obsWebSocket
            output:simpleobsws.RequestResponse = obsWebSocket.makeRequest("GetStreamStatus", {})
            print(output)
            if output.responseData.get("outputBytes", None) == None:
                return "[Is OBS Running?]"
            if output.responseData.get("outputDuration", None) == None:
                return "[Is OBS Running?]"
            if output.responseData.get("outputReconnecting", None) == None:
                return "[Is OBS Running?]"

            if output.responseData.get("outputReconnecting", None) == True:
                return " OBS is Reconnecting"

            total_duration_miliseconds = output.responseData.get("outputDuration", 0)
            total_bytes = output.responseData.get("outputBytes", 0)
            selected_interval = 30

            if total_duration_miliseconds != 0:
                # Calculate the bitrate
                bitrate = (total_bytes*8) / (total_duration_miliseconds/1000)
                bitrate_kbs = bitrate / 1000
                return "Average Bitrate: %s kbs" % (int(bitrate_kbs))



        except Exception as e:
            # todo handle exceptions
            return str(e)

        return ""
