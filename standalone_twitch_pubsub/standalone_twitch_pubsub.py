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

import re
from json import loads
from urllib.parse import urlencode

import requests

import credentials
import config

from channel_rewards.channelRewards_base import AbstractChannelRewards
import channel_rewards.channelRewards_base

import twitchAPI
from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.types import AuthScope
from twitchAPI.oauth import UserAuthenticator
from pprint import pprint
from uuid import UUID

from bot_functions.cooldowns import Cooldown_Module

import os
import bot_functions.praxis_logging as praxis_logging
praxis_logger_obj = praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

class Twitch_Pubsub():
    def __init__(self):
        super().__init__()
        self.credential : credentials.Twitch_Credential()
        self.twitch : Twitch()
        self.pubsub: PubSub()
        self.target_scope = [AuthScope.WHISPERS_READ, AuthScope.CHANNEL_READ_REDEMPTIONS, AuthScope.BITS_READ, AuthScope.CHANNEL_READ_SUBSCRIPTIONS]

        self.uuid_whisper = None
        self.uuid_channelPoints = None
        self.uuid_bits = None
        self.uuid_subs = None

        self.cooldownModule: Cooldown_Module = Cooldown_Module()
        self.cooldownModule.setupCooldown("twitchpubsub", 20, 32)

    def setup(self):
        self.twitch.authenticate_app(self.target_scope)

        self.twitch.set_user_authentication(self.credential.pubsub_AccessToken, self.target_scope, self.credential.pubsub_RefreshToken)

    def get_tokens(self):
        self.twitch.authenticate_app(self.target_scope)
        for scope_ in self.target_scope:
            print(scope_)
        auth = UserAuthenticator(self.twitch, self.target_scope, force_verify=True)
        token, refresh_token = auth.authenticate()

        if token is not None: print("found token")
        if refresh_token is not None: print("found refresh_token")
        print(token)
        print(refresh_token)

        self.twitch.set_user_authentication(token, self.target_scope, refresh_token)

    def start(self):
        self.pubsub = PubSub(self.twitch)
        #self.pubsub.ping_frequency = 30
        self.pubsub.start()
        print("started")

    def next(self):
        user_id = self.twitch.get_users(logins=[config.autoJoin_TwitchChannel])['data'][0]['id']
        if user_id is not None: print("found user_id")
        print(user_id)
        self.uuid_whisper = self.pubsub.listen_whispers(user_id, self.callback_whisper)
        self.uuid_channelPoints = self.pubsub.listen_channel_points(user_id, self.callback_channelPoints)
        self.uuid_bits = self.pubsub.listen_bits(user_id, self.callback_bits)
        self.uuid_subs = self.pubsub.listen_channel_subscriptions(user_id, self.callback_subs)
        #input('press ENTER to close...')

    def stop(self):
        self.pubsub.unlisten(self.uuid_whisper)
        self.pubsub.unlisten(self.uuid_channelPoints)
        self.pubsub.unlisten(self.uuid_bits)
        self.pubsub.unlisten(self.uuid_subs)
        self.pubsub.stop()

    def callback_whisper(self, uuid: UUID, data: dict) -> None:
        print('got callback for UUID ' + str(uuid))
        pprint(data)

    def callback_channelPoints(self, uuid: UUID, data: dict) -> None:
        print("Channel Point Redemption")
        print('got callback for UUID ' + str(uuid))
        pprint(data)
        #print("attempting to get data: ")
        #print(data['data']['redemption']['user']['display_name'])
        #print(data['data']['redemption']['reward']['title'])
        #print(data['data']['redemption']['reward']['prompt'])
        try:
            userinput = data['data']['redemption']['user_input']
        except:
            userinput = ""
        praxis_logger_obj.log("\n\n")
        praxis_logger_obj.log(data['data']['redemption']['user']['display_name'])
        praxis_logger_obj.log(data['data']['redemption']['reward']['title'])
        praxis_logger_obj.log(AbstractChannelRewards.ChannelRewardsType.channelPoints)
        praxis_logger_obj.log(data['data']['redemption']['reward']['prompt'])
        praxis_logger_obj.log(userinput)
        praxis_logger_obj.log(data)
        self.callback_EXEC(
            data['data']['redemption']['user']['display_name'],
            data['data']['redemption']['reward']['title'],
            AbstractChannelRewards.ChannelRewardsType.channelPoints,
            data['data']['redemption']['reward']['prompt'],
            userinput,
            data)


    def callback_bits(self, uuid: UUID, data: dict) -> None:
        print("Bits Redemption")
        print('got callback for UUID ' + str(uuid))
        pprint(data)

        praxis_logger_obj.log(data['data']['user_name'])

        try:
            userinput = data['data']['chat_message']
            praxis_logger_obj.log(data['data']['chat_message'])
        except:
            userinput = ""
        praxis_logger_obj.log(data)

        self.callback_EXEC(
            data['data']['user_name'],
            "TwitchBits",
            AbstractChannelRewards.ChannelRewardsType.twitch_bits,
            userinput,
            data['data']['bits_used'],
            data)

    def callback_subs(self, uuid: UUID, data: dict) -> None:
        print("Subs Redemption")
        print('got callback for UUID ' + str(uuid))
        pprint(data)

        try:
            userinput = data['message']['sub_message']['message']
        except:
            userinput = ""

        self.callback_EXEC(
            data['message']['display_name'],
            "TwitchSub",
            AbstractChannelRewards.ChannelRewardsType.twitch_subs,
            userinput,
            "",
            data)

    def callback_EXEC(self, sender, rewardName:str, rewardType, rewardPrompt, userInput, raw_data):
        try:
            is_actionable = self.is_reward(rewardName, rewardType)
            if is_actionable:
                praxis_logger_obj.log("Trying to do the thing")
                #if self.cooldownModule.isCooldownActive("twitchpubsub") == False:
                self.exec_reward(sender, rewardName, rewardType, rewardPrompt, userInput, raw_data)
        except:
            print("something went wrong with a reward")

    def is_reward(self, rewardName, rewardType):
        # todo need to url-escape word
        clean_param = urlencode({'reward_name': rewardName, 'reward_type':rewardType})
        print(rewardName, rewardType)
        #standalone_channelrewards
        url = "http://standalone_channelrewards:42069/api/v1/reward?%s" % clean_param
        resp = requests.get(url)
        return resp.status_code == 200

    def exec_reward(self, sender, rewardName, rewardType, rewardPrompt, userInput, realMessage):
        params = urlencode(
            {'reward_source': channel_rewards.channelRewards_base.AbstractChannelRewards.ChannelRewardsSource.Twitch,
            'user_name': sender,
            'reward_name': rewardName,
            'reward_type': rewardType,
            'reward_prompt': rewardPrompt,
            'user_input' : userInput,
            'bonus_data': realMessage})

        #standalone_channelrewards
        url = "http://standalone_channelrewards:42069/api/v1/exec_reward?%s" % params
        resp = requests.get(url)
        if resp.status_code == 200:
            print("Got the following message: %s" % resp.text)
            data = loads(resp.text)
            msg = data['message']
            if msg is not None:
                #self.send_message(msg) #Cant Send messages with this pubsub library afaik
                pass
        else:
            # todo handle failed requests
            pass

    #FINISH THIS EVENT LOG
    def send_EventLog(self, eventName, eventTime, eventType, eventSender, eventData):
        params = urlencode(
            {'event_name': eventName,
            'event_time': eventTime,
            'event_type': eventType,
            'eventSender': eventSender,
            'event_data': eventData})
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

if __name__ == "__main__":
    testModule = Twitch_Pubsub()

    credentials_manager = credentials.Credentials_Module()
    credentials_manager.load_credentials()
    testModule.credential = credentials_manager.find_Twitch_Credential(config.credentialsNickname)
    testModule.twitch = Twitch(testModule.credential.pubsub_client_id, testModule.credential.pubsub_secret)
    #pprint(testModule.twitch.get_users(logins=['thecuriousnerd']))

    #testModule.get_tokens()
    testModule.setup()
    testModule.start()
    testModule.next()
    #testModule.stop()