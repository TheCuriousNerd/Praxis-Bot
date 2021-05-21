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

import json
import flask
from flask import Flask, request, after_this_request

from ..commands import loader as command_loader
from ..commands.command_base import AbstractCommand

from json import loads
from urllib.parse import urlencode

import requests

import base64

import os
from ..bot_functions import praxis_logging as praxis_logging
praxis_logger_obj = praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

api = flask.Flask(__name__)
# enable/disable this to get web pages of crashes returned
api.config["DEBUG"] = False

loadedCommands = {}

def init():
    # todo load entire command library and cache it here
    load_commands()


def load_commands():
    global loadedCommands
    loadedCommands = command_loader.load_commands(AbstractCommand.CommandType.Ver2)


def is_command(command: str) -> bool:
    #print(command)
    for cmd in loadedCommands:
        #print(cmd)
        if command == cmd:
            return True

    if command == "!echo":
        return True
    else:
        return False

def handle_command(source, username, command, rest, bonusData):
    if command == "!echo":
        message = "Got payload [%s]" % rest
        #print(message)
        return flask.make_response("{\"message\":\"%s\"}" % message, 200, {"Content-Type": "application/json"})

    tempSource = source.replace('CommandSource.', '')
    realSource = AbstractCommand.CommandSource.__dict__[tempSource]
    cmd:AbstractCommand = loadedCommands[command]
    if cmd is not None:
        cmd_response = cmd.do_command(source, username, command, rest, bonusData)
        return flask.make_response("{\"message\":\"%s\"}" % cmd_response, 200, {"Content-Type": "application/json"})

    #print("Doing a command")

def handle_get_list():
    tempDict = {}
    returnedDict = {}

    for cmd in loadedCommands:
        tempCmd:AbstractCommand = loadedCommands[cmd]
        tempDict['command'] = tempCmd.command
        tempDict['isCommandEnabled'] = str(tempCmd.isCommandEnabled).lower()
        returnedDict[tempCmd.command] = tempDict
        tempDict = {}

    payload = json.dumps(returnedDict)
    praxis_logger_obj.log("dumped")
    praxis_logger_obj.log(payload)
    payload = base64.b64encode(str.encode(payload))
    print("encoded")
    praxis_logger_obj.log("encoded")
    praxis_logger_obj.log(payload)
    return flask.make_response("{\"message\":\"%s\"}" % payload.decode(), 200, {"Content-Type": "application/json"})

@api.route('/api/v1/command', methods=['GET'])
def command_check():
    if 'name' in request.args:
        if is_command(request.args['name']):
            return flask.make_response('', 200)
        else:
            return flask.make_response('', 404)


@api.route('/api/v1/exec_command', methods=['GET'])
def exec_command():
    if 'command_name' not in request.args:
        return flask.make_response('{\"text\":"Argument \'command_name\' not in request"}', 400)
    if 'rest' not in request.args:
        return flask.make_response('{\"text\":"Argument \'rest\' not in request"}', 400)

    if 'command_source' not in request.args:
        return flask.make_response('{\"text\":"Argument \'command_source\' not in request"}', 400)

    if 'user_name' not in request.args:
        username = "User"
    else:
        username = request.args['user_name']

    return handle_command(request.args['command_source'], username, request.args['command_name'], request.args['rest'], request.args['bonus_data'])

@api.route('/api/v1/get_list/all', methods=['GET'])
def get_list():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    return handle_get_list()

if __name__ == '__main__':
    init()
    api.run(host='0.0.0.0', port=12310)
