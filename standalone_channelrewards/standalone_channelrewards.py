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

import flask
from flask import Flask, request, after_this_request

import channel_rewards.channelRewards_loader as rewards_loader
from channel_rewards.channelRewards_base import AbstractChannelRewards

from json import loads
from urllib.parse import urlencode

import requests

import json
import base64

import os
import bot_functions.praxis_logging as praxis_logging
praxis_logger_obj = praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

api = flask.Flask(__name__)
# enable/disable this to get web pages of crashes returned
api.config["DEBUG"] = False

loadedRewards = {}

def init():
    # todo load entire reward library and cache it here
    praxis_logger_obj.log("init stuff")
    loadedRewards[AbstractChannelRewards.ChannelRewardsType.channelPoints] = rewards_loader.load_rewards(AbstractChannelRewards.ChannelRewardsType.channelPoints)
    loadedRewards[AbstractChannelRewards.ChannelRewardsType.twitch_bits] = rewards_loader.load_rewards(AbstractChannelRewards.ChannelRewardsType.twitch_bits)
    loadedRewards[AbstractChannelRewards.ChannelRewardsType.twitch_subs] = rewards_loader.load_rewards(AbstractChannelRewards.ChannelRewardsType.twitch_subs)


def is_reward(reward_name, reward_type) -> bool:
    #global loadedRewards
    tempType = reward_type.replace('ChannelRewardsType.', '')
    realTempType = AbstractChannelRewards.ChannelRewardsType.__dict__[tempType]
    #praxis_logger_obj.log(loadedRewards[realTempType])

    for reward in loadedRewards[realTempType]:
        #praxis_logger_obj.log("found: ", reward, "type: ", type(reward))
        if reward_name == reward:
            praxis_logger_obj.log("Equal")
            return True


    if reward_name == "!echo":
        return True
    else:
        return False


def handle_reward(source, username, reward_name, reward_type, rewardPrompt, userInput, bonusData):
    #reward:AbstractChannelRewards = loadedRewards[reward_name]
    praxis_logger_obj.log("\n trying to handle reward: " + reward_name)
    try:
        tempType = reward_type.replace('ChannelRewardsType.', '')
        realTempType = AbstractChannelRewards.ChannelRewardsType.__dict__[tempType]
        tempSource = source.replace('ChannelRewardsSource.', '')
        realSource = AbstractChannelRewards.ChannelRewardsSource.__dict__[tempSource]
        reward:AbstractChannelRewards = loadedRewards[realTempType][reward_name]
        if reward is not None:
            reward_response = reward.do_ChannelReward(realSource, username, reward_name, rewardPrompt, userInput, bonusData)
            return flask.make_response("{\"message\":\"%s\"}" % reward_response, 200, {"Content-Type": "application/json"})
    except:
        return flask.make_response("{\"message\":\"%s\"}" % "Something Went horribly wrong", 500)
    #praxis_logger_obj.log("Doing a reward")

def handle_get_list():
    tempDict = {}
    returnedDict = {}

    for cmd in loadedRewards[AbstractChannelRewards.ChannelRewardsType.channelPoints]:
        tempCmd:AbstractChannelRewards = loadedRewards[AbstractChannelRewards.ChannelRewardsType.channelPoints][cmd]
        tempDict['channelRewardName'] = tempCmd.ChannelRewardName
        tempDict['isRewardEnabled'] = str(tempCmd.isChannelRewardEnabled).lower()
        returnedDict[tempCmd.ChannelRewardName] = tempDict
        tempDict = {}
    for cmd in loadedRewards[AbstractChannelRewards.ChannelRewardsType.twitch_bits]:
        tempCmd:AbstractChannelRewards = loadedRewards[AbstractChannelRewards.ChannelRewardsType.twitch_bits][cmd]
        tempDict['channelRewardName'] = tempCmd.ChannelRewardName
        tempDict['isRewardEnabled'] = str(tempCmd.isChannelRewardEnabled).lower()
        returnedDict[tempCmd.ChannelRewardName] = tempDict
        tempDict = {}
    for cmd in loadedRewards[AbstractChannelRewards.ChannelRewardsType.twitch_subs]:
        tempCmd:AbstractChannelRewards = loadedRewards[AbstractChannelRewards.ChannelRewardsType.twitch_subs][cmd]
        tempDict['channelRewardName'] = tempCmd.ChannelRewardName
        tempDict['isRewardEnabled'] = str(tempCmd.isChannelRewardEnabled).lower()
        returnedDict[tempCmd.ChannelRewardName] = tempDict
        tempDict = {}

    payload = json.dumps(returnedDict)
    praxis_logger_obj.log("dumped")
    praxis_logger_obj.log(payload)
    payload = base64.b64encode(str.encode(payload))
    print("encoded")
    praxis_logger_obj.log("encoded")
    praxis_logger_obj.log(payload)
    return flask.make_response("{\"message\":\"%s\"}" % payload.decode(), 200, {"Content-Type": "application/json"})


@api.route('/api/v1/reward', methods=['GET'])
def reward_check():
    if 'reward_name' in request.args and 'reward_type' in request.args:
        #praxis_logger_obj.log("reward_name: "+ request.args['reward_name']+"reward_type: "+ request.args['reward_type'])
        if is_reward(request.args['reward_name'], request.args['reward_type']):
            praxis_logger_obj.log("about to send")
            return flask.make_response('', 200)
        else:
            return flask.make_response('', 404)


@api.route('/api/v1/exec_reward', methods=['GET'])
def exec_reward():
    if 'reward_name' not in request.args:
        return flask.make_response('{\"text\":"Argument \'reward_name\' not in request"}', 400)
    if 'reward_type' not in request.args:
        return flask.make_response('{\"text\":"Argument \'reward_type\' not in request"}', 400)
    if 'reward_prompt' not in request.args:
        return flask.make_response('{\"text\":"Argument \'reward_prompt\' not in request"}', 400)
    if 'user_input' not in request.args:
        return flask.make_response('{\"text\":"Argument \'user_input\' not in request"}', 400)


    if 'reward_source' not in request.args:
        return flask.make_response('{\"text\":"Argument \'reward_source\' not in request"}', 400)

    if 'user_name' not in request.args:
        username = "User"
    else:
        username = request.args['user_name']
    praxis_logger_obj.log("\n About to try a reward")

    praxis_logger_obj.log(request.args['reward_source'])
    praxis_logger_obj.log(request.args['reward_name'])
    praxis_logger_obj.log(request.args['reward_type'])
    praxis_logger_obj.log(request.args['reward_prompt'])
    praxis_logger_obj.log(request.args['user_input'])
    praxis_logger_obj.log(request.args['bonus_data'])
    return handle_reward(
        request.args['reward_source'],
        username,
        request.args['reward_name'],
        request.args['reward_type'],
        request.args['reward_prompt'],
        request.args['user_input'],
        request.args['bonus_data'])

@api.route('/api/v1/get_list/all', methods=['GET'])
def get_list():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    return handle_get_list()

if __name__ == '__main__':
    init()
    api.run(host='0.0.0.0', port=42069)
