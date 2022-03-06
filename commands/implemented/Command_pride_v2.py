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

import threading

import random

import os
import bot_functions.praxis_logging as praxis_logging
praxis_logger_obj = praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

class Command_pride_v2(AbstractCommand, metaclass=ABCMeta):
    """
    this is the pride command.
    """
    command = "!pride"

    def __init__(self):
        super().__init__(Command_pride_v2.command, n_args=1, command_type=AbstractCommand.CommandType.Ver2)
        self.help = ["This is a pride command.",
        "\nExample:","!pride \"SCENE\"","lights \"COLOR\"","lights \"R\" \"G\" \"B\"","lights \"1\" \"0.5\" \"0\""]
        self.isCommandEnabled = True
        self.threads = []

    def do_command(self, source = AbstractCommand.CommandSource.default, user = "User", userID = "0",  command = "", rest = "", bonusData = None):
        returnString = ""
        praxis_logger_obj.log("\n Command>: " + command + rest)
        isTwitch = False


        #print("sending:",user, 16, "!lights hydration")
        try:
            try:
                if self.is_command_enabled:
                    thread_ = threading.Thread(target=self.send_Lights_Command, args=(user, 16, "!lights ravemode", ""))
                    thread_.daemon = True
                    self.threads.append(thread_)
                    thread_.start()
            except:
                if self.is_command_enabled:
                    thread_ = threading.Thread(target=self.send_TTS, args=("", "Silly Nerd Fix The Lights Module"))
                    thread_.daemon = True
                    self.threads.append(thread_)
                    thread_.start()
            try:
                if self.is_command_enabled:
                    prompt_ = self.get_Phrase("wishes everyone a happy pride month!")
                    thread_ = threading.Thread(target=self.send_TTS, args=("", user + prompt_))
                    thread_.daemon = True
                    self.threads.append(thread_)
                    thread_.start()
                    returnString = user + " " + prompt_
            except:
                pass
        except:
            pass


        return returnString

    def send_Lights_Command(self, username, light_group, command, rest):
        # todo need to url-escape command and rest
        params = urlencode({'user_name': username, 'light_group': light_group, 'command': command, 'rest':rest})
        #standalone-lights
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
        #standalone-tts-core
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

    def get_Phrase(self, defaultRewardPrompt,
    phrases = ["is hyped for pride!"]):

        phrases.append(defaultRewardPrompt)
        totalPhrases = len(phrases) - 1
        targetPhrase = phrases[random.randint(0,totalPhrases)]
        return targetPhrase

    def get_help(self):
        return self.help

    def get_help(self):
        return self.help