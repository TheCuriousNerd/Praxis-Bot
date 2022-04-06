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
from bot_functions.chyron_module import Chyron_Module

from commands import loader as command_loader
from commands import loader_functions as function_loader
from commands.command_base import AbstractCommand
from commands.command_functions import AbstractCommandFunction, Abstract_Function_Helpers

from json import loads
from urllib.parse import urlencode

import requests

import base64

import os
import bot_functions.praxis_logging as praxis_logging

import bot_functions.container_stats_api as container_stats_api
container_stats_api.main()

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
    global loadedCommands_v3
    global loadedFunctions
    loadedCommands = command_loader.load_commands(AbstractCommand.CommandType.Ver2)
    loadedCommands_v3 = command_loader.load_commands(AbstractCommand.CommandType.Ver3)
    loadedFunctions = function_loader.load_functions(AbstractCommandFunction.FunctionType.ver0)
    for f in loadedFunctions:
        praxis_logger_obj.log("loadedFunctions: ")
        praxis_logger_obj.log(str(f))

def is_command(command: str) -> bool:
    #print(command)
    isCommand = False
    for cmd in loadedCommands:
        #print(cmd)
        if command == cmd:
            isCommand = True

    v3helper = Abstract_Function_Helpers()
    v3CommandResponse = v3helper.get_Command_returnString(command, praxis_logger_obj)
    praxis_logger_obj.log("command: ")
    praxis_logger_obj.log(command)

    #praxis_logger_obj.log("v3Command: ")
    #praxis_logger_obj.log(v3Command)

    if v3CommandResponse is not None:
        isCommand = True
        praxis_logger_obj.log("v3Command: ")
        praxis_logger_obj.log(v3CommandResponse)

    if command == "!echo":
        isCommand = True

    if isCommand == True:
        log_ = "%s is a recognized command" % command
        praxis_logger_obj.log(log_)
        return True
    else:
        log_ = "%s is not a recognized command" % command
        praxis_logger_obj.log(log_)
        return False

def handle_command(source, username, userID, command, rest, bonusData):
    praxis_logger_obj.log("trying to handle command:")
    praxis_logger_obj.log(command)

    if command == "!echo":
        message = "Got payload [%s]" % rest
        #print(message)
        return flask.make_response("{\"message\":\"%s\"}" % message, 200, {"Content-Type": "application/json"})

    tempSource = source.replace('CommandSource.', '')
    realSource = AbstractCommand.CommandSource.__dict__[tempSource]

    cmd = None
    cmd_v3 = None

    v3Flag = False
    v3helper = Abstract_Function_Helpers()
    v3cmd_response = v3helper.get_Command_returnString(command, praxis_logger_obj)
    try:
        if v3cmd_response is None:
            cmd:AbstractCommand = loadedCommands[command]
            #print(type(cmd))
            #print(cmd.command)
            praxis_logger_obj.log("RUNNING cmd from loadedCommands")
            praxis_logger_obj.log(cmd)
    except:
        pass
    try:
        if v3cmd_response is not None:
            v3Flag = True
            cmd_v3:AbstractCommand = loadedCommands_v3["base_v3"]
            #print(type(cmd_v3))
            #print(cmd_v3.command)
            praxis_logger_obj.log("RUNNING cmd from loadedCommands_v3")
            praxis_logger_obj.log(cmd_v3)
    except:
        pass

    if v3Flag is True:
        if cmd_v3 is not None:
            cmd_v3.loadedFunctions = loadedFunctions
            # praxis_logger_obj.log("RUNNING COMMAND...")
            # praxis_logger_obj.log(tempSource)
            # praxis_logger_obj.log(username)
            # praxis_logger_obj.log(userID)
            # praxis_logger_obj.log(command)
            # praxis_logger_obj.log(rest)
            # praxis_logger_obj.log(bonusData)

            cmd_results_v3 = cmd_v3.do_command(tempSource, username, userID, command, rest, bonusData)
            praxis_logger_obj.log("COMMAND RESULTS V3:")
            praxis_logger_obj.log(cmd_results_v3)
            return flask.make_response("{\"message\":\"%s\"}" % cmd_results_v3, 200, {"Content-Type": "application/json"})
    else:
        if cmd is not None:
            cmd_response = cmd.do_command(tempSource, username, userID, command, rest, bonusData)
            praxis_logger_obj.log("COMMAND RESULTS:")
            praxis_logger_obj.log(cmd_response)
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


# ======================================================================================================================
# API ENDPOINTS
# ======================================================================================================================


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

    if 'user_id' not in request.args:
        userID = "0"
    else:
        userID = request.args['user_id']

    return handle_command(request.args['command_source'], username, userID, request.args['command_name'], request.args['rest'], request.args['bonus_data'])

@api.route('/api/v1/get_list/all', methods=['GET'])
def get_list():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    return handle_get_list()



@api.route('/api/v1/chyron/get', methods=['GET'])
def get_chyron():
    # if 'chyron_name' not in request.args: # This is for later when we have multiple chyron types
    #     pass
    #     #return flask.make_response('{\"text\":"Argument \'chyron_name\' not in request"}', 400)
    module = Chyron_Module()
    chyronString = module.getChyronString()
    return flask.make_response(chyronString, 200)

@api.route('/api/v1/chyron/update_file', methods=['GET'])
def update_chyron_file():
    # if 'chyron_name' not in request.args: # This is for later when we have multiple chyron types
    #     pass
    #     #return flask.make_response('{\"text\":"Argument \'chyron_name\' not in request"}', 400)
    module = Chyron_Module()
    module.updateChyronFile()
    return flask.make_response("done", 200)



if __name__ == '__main__':
    init()
    api.run(host='0.0.0.0', port=42010)
