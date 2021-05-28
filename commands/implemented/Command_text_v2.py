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

from bot_functions import tempText_Module as tempText_Module

import os
import bot_functions.praxis_logging as praxis_logging
praxis_logger_obj = praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

class Command_Text_v2(AbstractCommand, metaclass=ABCMeta):
    """
    this is the text command.
    """
    command = "!text"

    def __init__(self):
        super().__init__(Command_Text_v2.command, n_args=1, command_type=AbstractCommand.CommandType.Ver2)
        self.help = ["The temptext string can be generated and updated with this command.",
        "\nExample:","temptext update \"Name\" \"Title\" \"Content\""]
        self.isCommandEnabled = True

    def do_command(self, source = AbstractCommand.CommandSource.default, user = "User",  command = "", rest = "", bonusData = None):
        returnString = "trying to update text..."
        praxis_logger_obj.log("\n Command>: " + command + " " + rest)
        returnString = user + " has attempted to update the text but an error may have occurred!"
        for name in config.adminUsers_List:
            print(name)
            tempName = user.lower()
            if name == tempName:

                #try:
                #    returnString = user + " has updated the text!"
                #    tempText_ = tempText_Module.tempText_Module()
                #    tempText_.main()
                #    testItem = tempText_Module.tempTextItem("testy","► ", rest)
                #    tempText_.makeItem(testItem)
                #    tempText_.update_tempTextFiles()
                #except:
                #    returnString = user + " has attempted to update the text but an error may have occurred!"
                #returnString = chyron_.chyron_computedString


                bandaid_string:str = command + " " + rest
                tempParsedMessage = bandaid_string.split(" ")
                i = len(tempParsedMessage)
                if i > 2:
                    if "update" in tempParsedMessage[1]:
                        tempTextModule:tempText_Module.tempText_Module = tempText_Module.tempText_Module()
                        tempText:tempText_Module.tempTextItem = tempText_Module.tempTextItem()
                        if i > 2:
                            newText = ""
                            counter = 0
                            for word in tempParsedMessage:
                                if counter > 2:
                                    newText = newText + word + " "
                                counter = counter + 1
                            newText = newText[:-1] # Gets rid of last space
                            #print(tempParsedMessage[2], newText)
                            tempText.itemName = tempParsedMessage[2]
                            tempText.itemContent = newText
                            tempTextModule.makeItem(tempText)
                            returnString = user + " has updated the text!"
                        else:
                            returnString = user + " has attempted to update the text but an error may have occurred!"
                        #tempTextModule.update_tempTextFiles()
                    if "chyron" in tempParsedMessage[1]:
                        tempTextModule:tempText_Module.tempText_Module = tempText_Module.tempText_Module()
                        tempText:tempText_Module.tempTextItem = tempText_Module.tempTextItem()
                        if i > 1:
                            newText = ""
                            counter = 0
                            for word in tempParsedMessage:
                                if counter > 1:
                                    newText = newText + word + " "
                                counter = counter + 1
                            newText = newText[:-1] # Gets rid of last space
                            #print(tempParsedMessage[2], newText)
                            tempText.itemName = tempParsedMessage[1]
                            if len(newText) < 180:
                                #for x in range(120 - len(newText)):
                                #    newText = newText + " "
                                while len(newText) < 180:
                                    newText = newText + " "

                            tempText.itemContent = newText
                            tempTextModule.makeItem(tempText)
                            returnString = user + " has updated the chyron text!"
                        else:
                            returnString = user + " has attempted to update the text but an error may have occurred!"
                    #tempTextModule.update_tempTextFiles()




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