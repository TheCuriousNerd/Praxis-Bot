# The main repository of Praxis Bot can be found at: <https://github.com/TheCuriousNerd/Praxis-Bot>.
# Copyright (C) 2021

# Author Info Examples:
# Name / Email / Website
# Twitter / Twitch / Youtube

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

from datetime import datetime
import re
from json import loads
from urllib.parse import urlencode

import requests
import twitch
import twitch.chat

import config as config
import credentials
from bot_functions.cooldowns import Cooldown_Module
import commands.command_base
import bot_functions.utilities_script as utility

import os
import bot_functions.praxis_logging as praxis_logging
praxis_logger_obj = praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

class Twitch_Module():
    def __init__(self):
        super().__init__()
        self.twitchCredential: credentials.Twitch_Credential
        self.chat: twitch.Chat

        self.block_chat_url: bool = True
        self.whitelisted_users: list = ["thecuriousnerd"]
        # don't freak out, this is *merely* a regex for matching urls that will hit just about everything
        self._urlMatcher = re.compile(
            "(https?:(/{1,3}|[a-z0-9%])|[a-z0-9.-]+[.](com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw))")

        # Default Twitch Chat limit is 20 per 30 seconds
        # If Mod or Op, Twitch Chat limit is 100 per 30 seconds
        self.cooldownModule: Cooldown_Module = Cooldown_Module()
        self.cooldownModule.setupCooldown("twitchChat", 20, 32)

    def join_channel(self, credential: credentials.Twitch_Credential, channel_name: str):
        channel_name = "#" + channel_name
        print("Connecting to Channel: " + channel_name + "...")

        if credential is None:
            credential = self.twitchCredential

        self.chat = twitch.Chat(
            channel=channel_name,
            nickname=credential.username,
            oauth=credential.oauth,
            # LIBRARY UPDATE BROKE THE FOLLOWING LINE [FIX THIS]
            # helix = twitch.Helix(credential.helix, use_cache=True)
        )
        self.chat.subscribe(self.twitch_chat)

        print("Connected to Channel: ", channel_name)

    def leave_channel(self):
        print("Leaving Channel", self.chat.channel)
        self.chat.irc.leave_channel(self.chat.channel)
        self.chat.irc.socket.close()

    def send_message(self, message):
        isBlocked = self.isChannel_inConfigList(self.chat.channel, config.block_TwitchChannelsMessaging)
        # print("isBlocked: " + str(isBlocked) + " for: " + self.chat.channel)
        #if self.
        if utility.contains_slur(message): isBlocked = True

        if self.cooldownModule.isCooldownActive(
                "twitchChat") == False and not isBlocked and not config.blockAll_TwitchChatChannelsMessaging:
            self.chat.send(message)
            # print("Sent ChatMSG")
            self.cooldownModule.actionTrigger("twitchChat")

    def eval_command(self, message):
        command, rest = utility.parse_line(message.text)

        try:
            is_actionable = self.is_command(command)
            if is_actionable:
                self.send_EventLog(command, str(datetime.now()), "command.twitch", message.sender, rest)
                praxis_logger_obj.log("Sent a thing")
        except:
            praxis_logger_obj.log("something went wrong with Event LOG")
        try:
            is_actionable = self.is_command(command)
            if is_actionable:
                if self.cooldownModule.isCooldownActive("twitchChat") == False:
                        self.exec_command(message ,command, rest)
        except:
            praxis_logger_obj.log("something went wrong with a command")

    def is_command(self, word: str) -> bool:
        # todo need to url-escape word
        clean_param = urlencode({'name': word})
        url = "http://standalone_command:42010/api/v1/command?%s" % clean_param
        resp = requests.get(url)
        return resp.status_code == 200

    def exec_command(self, realMessage: twitch.chat.Message, command: str, rest: str):
        # todo need to url-escape command and rest
        params = urlencode(
            {'command_source': commands.command_base.AbstractCommand.CommandSource.Twitch,
            'user_name': realMessage.sender,
            'command_name': command,
            'rest': rest,
            'bonus_data': realMessage})
        #standalone_command
        url = "http://standalone_command:42010/api/v1/exec_command?%s" % params
        resp = requests.get(url)
        if resp.status_code == 200:
            print("Got the following message: %s" % resp.text)
            data = loads(resp.text)
            msg = data['message']
            if msg is not None:
                self.send_message(msg)
        else:
            # todo handle failed requests
            pass

    def eval_tts(self, message: twitch.chat.Message):
        command, rest = utility.parse_line(message.text)
        try:
            is_actionable = self.is_command(command)
            if not is_actionable:
                self.exec_tts(message)
        except:
            print("something went wrong with tts")

    def exec_tts(self, message: twitch.chat.Message):

        if config.autoEnabled_TwitchTTS:
            if config.autoEnabled_TwitchTTS_SpeakersList_Only:
                tempName = message.sender.lower()
                if tempName in config.allowedTTS_List:
                    text_to_say: str = "%s says, %s" % (message.sender, message.text)
                    self.exec_tts_sender("", text_to_say)
            else:
                text_to_say: str = "%s says, %s" % (message.sender, message.text)
                self.exec_tts_sender("", text_to_say)

    def send_EventLog(self, command, eventTime, eventType, eventSender, rest):
        params = urlencode(
            {'event_name': command,
            'event_time': eventTime,
            'event_type': eventType,
            'eventSender': eventSender,
            'event_data': rest})
        url = "http://standalone_eventlog:42008/api/v1/event_log/add_event?%s" % params
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

    def exec_tts_sender(self, username, message):
        params = urlencode({'tts_sender': username, 'tts_text': message})
        #standalone_tts_core
        url = "http://localhost:42064/api/v1/tts/send_text?%s" % params
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

    def send_whisper(self, user, message):
        pass

    # This reacts to messages
    def twitch_chat(self, message: twitch.chat.Message) -> None:
        print("[#" + message.channel + "](" + message.sender + ")> " + message.text)
        command, rest = utility.parse_line(message.text)

        praxis_logger_obj.log("\n[#" + message.channel + "](" + message.sender + ")> " + message.text)

        self.eval_command(message)
        self.eval_tts(message)

    def isChannel_inConfigList(self, selectedChannel, selectedList):
        # print(channel)
        # print(selectedList)
        is_Self = False
        for twitchChannel in selectedList:
            if twitchChannel == selectedChannel:
                is_Self = True
        return is_Self


if __name__ == "__main__":
    testModule = Twitch_Module()

    credentials_manager = credentials.Credentials_Module()
    credentials_manager.load_credentials()
    testModule.twitchCredential = credentials_manager.find_Twitch_Credential(config.credentialsNickname)

    for twitchChannel in config.autoJoin_TwitchChannels:
        testModule.join_channel(None, twitchChannel)
