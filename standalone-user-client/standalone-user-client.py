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

from enum import Enum
from os import F_OK
from bot_functions  import tempText_Module as tempText_Module
import time
import config as config

from datetime import datetime
import re
from json import loads
from urllib.parse import urlencode

import requests

import flask
from flask import Flask, request, after_this_request

import credentials

from bot_functions.cooldowns import Cooldown_Module

import bot_functions.utilities_script as utility

import bot_functions.chyron_module as chyron_module
import bot_functions.timers_module as timers_module

import random

import os
import bot_functions.praxis_logging as praxis_logging
praxis_logger_obj = praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

api:Flask = Flask(__name__)
api.config["DEBUG"] = True


def init():
    print("starting up... ",)


def handle_request_get(requestName, requestType, requestData):

    if requestType == "list":
        if requestName == "Chyron":
            response = request_get_list("XXXXXXXXX", "42010")
            return flask.make_response("{\"message\": \"%s\"}" % response, 200, {"Content-Type": "application/json"})
        if requestName == "Commands":
            response = request_get_list("standalone-command", "42010")
            return flask.make_response("{\"message\": \"%s\"}" % response, 200, {"Content-Type": "application/json"})
        if requestName == "Rewards":
            response = request_get_list("standalone-channelrewards", "42069")
            return flask.make_response("{\"message\": \"%s\"}" % response, 200, {"Content-Type": "application/json"})
        if requestName == "Timers":
            response = request_get_list("XXXXXXXXX", "42010")
            return flask.make_response("{\"message\": \"%s\"}" % response, 200, {"Content-Type": "application/json"})
        if requestName == "TextSources":
            response = request_get_list("XXXXXXXXX", "42010")
            return flask.make_response("{\"message\": \"%s\"}" % response, 200, {"Content-Type": "application/json"})
        if requestName == "EventHistory":
            params = urlencode(
            {'request_name': requestName,
            'request_type': requestType,
            'request_data': requestData})
            response = request_get_eventlist(params)
            return flask.make_response("{\"message\": \"%s\"}" % response, 200, {"Content-Type": "application/json"})
        else:
            return flask.make_response("{\"message\": \"%s\"}" % "Invalid Request Name", 400, {"Content-Type": "application/json"})

def request_get_list(serviceName, servicePort):
    try:
        url = "http://"+ serviceName + ":"+ servicePort + "/api/v1/get_list/all"
        resp = requests.get(url)

        if resp.status_code == 200:
            print("Got the following message: %s" % resp.text)
            data = loads(resp.text)
            msg = data['message']
            if msg is not None:
                praxis_logger_obj.log(msg)
                return msg
                # todo send to logger and other relevent services
        else:
            # todo handle failed requests
                return flask.make_response("{\"message\": \"%s\"}" % "Minor Mess up on get list", 200, {"Content-Type": "application/json"})
    except:
        return flask.make_response("{\"message\": \"%s\"}" % "Major Mess up on get list", 200, {"Content-Type": "application/json"})

def request_get_eventlist(params):
    try:
        url = "http://%s:%s/api/v1/event_log/get_events?%s" % (config.standalone_eventlog_address[0].get("ip"), config.standalone_eventlog_address[0].get("port"), params)
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
                return flask.make_response("{\"message\": \"%s\"}" % "Minor Mess up on get eventlist", 200, {"Content-Type": "application/json"})
    except:
        return flask.make_response("{\"message\": \"%s\"}" % "Major Mess up on get eventlist", 200, {"Content-Type": "application/json"})

def request_reRunEvent(eventName, eventTime, eventType, eventSender, eventData):
    try:
        params = urlencode(
            {'eventName': eventName,
            'eventTime': eventTime,
            'eventType': eventType,
            'eventSender': eventSender,
            'eventData': eventData})
        url = "http://%s:%s/api/v1/event_log/reRunEvent?%s" % (config.standalone_eventlog_address[0].get("ip"), config.standalone_eventlog_address[0].get("port"), params)
        resp = requests.get(url)

        if resp.status_code == 200:
            print("Got the following message: %s" % resp.text)
            data = loads(resp.text)
            msg = data['message']
            if msg is not None:
                return flask.make_response("{\"message\": \"%s\"}" % msg, 200, {"Content-Type": "application/json"})
                # todo send to logger and other relevent services
        else:
            # todo handle failed requests
                return flask.make_response('Something Went a little bit Wrong rerunning an event', 400)
    except:
        return flask.make_response('Something Went Wrong rerunning an event', 400)

def handle_request_set(requestName, requestType, requestData):
    if requestType == "update":
        if requestName == "Chyron":
            pass
        if requestName == "Commands":
            pass
    elif requestType == "delete":
        if requestName == "Chyron":
            pass
        if requestName == "Commands":
            pass


def handle_get_container_status():
    try:
        currentStatus = {}
        # standalone_db_manager
        # standalone_eventlog
        # standalone_user_client
        # standalone_websource
        # standalone_lights
        # standalone_tts_core
        # standalone_channelrewards
        # standalone_command
        # standalone_discord_script
        # standalone_twitch_script
        # standalone_twitch_pubsub
        params = urlencode(
        {'standalone_db_manager': currentStatus.get("standalone_db_manager"),
        'standalone_eventlog': currentStatus.get("standalone_eventlog"),
        'standalone_user_client': currentStatus.get("standalone_user_client"),
        'standalone_websource': currentStatus.get("standalone_websource"),
        'standalone_lights': currentStatus.get("standalone_lights"),
        'standalone_tts_core': currentStatus.get("standalone_tts_core"),
        'standalone_channelrewards': currentStatus.get("standalone_channelrewards"),
        'standalone_command': currentStatus.get("standalone_command"),
        'standalone_discord_script': currentStatus.get("standalone_discord_script"),
        'standalone_twitch_script': currentStatus.get("standalone_twitch_script"),
        'standalone_twitch_pubsub': currentStatus.get("standalone_twitch_pubsub")
        })
        response = request_get_eventlist(params)
        return flask.make_response("{\"message\": \"%s\"}" % response, 200, {"Content-Type": "application/json"})
    except:
        return flask.make_response("{\"message\": \"%s\"}" % "Something went wrong getting the status", 400, {"Content-Type": "application/json"})



@api.route('/')
def bot_StatusIcon():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    return flask.make_response('Client Service: OK', 200)

@api.route('/api/v1/user_client/get', methods=['GET'])
def get_data():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    if 'request_name' not in request.args:
        return flask.make_response('{\"text\":"Argument \'request_name\' not in request"}', 400)
    if 'request_type' not in request.args:
        return flask.make_response('{\"text\":"Argument \'request_type\' not in request"}', 400)
    if 'request_data' not in request.args:
        requestData = None
    else:
        requestData = request.args['request_data']

    return handle_request_get(request.args['request_name'], request.args['request_type'], requestData)

@api.route('/api/v1/user_client/set', methods=['GET'])
def set_data():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    if 'request_type' not in request.args:
        return flask.make_response('{\"text\":"Argument \'request_type\' not in request"}', 400)

@api.route('/api/v1/user_client/event_log/reRunEvent', methods=['GET'])
def EventLog_reRunEvent():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    if 'eventName' not in request.args:
        return flask.make_response('{\"text\":"Argument \'eventName\' not in request"}', 400)
    if 'eventTime' not in request.args:
        sentTime = request.args('eventTime')
    else:
        sentTime = None
    if 'eventType' not in request.args:
        return flask.make_response('{\"text\":"Argument \'eventType\' not in request"}', 400)
    if 'eventSender' not in request.args:
        return flask.make_response('{\"text\":"Argument \'eventSender\' not in request"}', 400)
    if 'eventData' not in request.args:
        return flask.make_response('{\"text\":"Argument \'eventData\' not in request"}', 400)

    #return flask.make_response("test", 200)
    return request_reRunEvent(request.args['eventName'], sentTime, request.args['eventType'], request.args['eventSender'], request.args['eventData'])

@api.route('/api/v1/user_client/containers/get_status', methods=['GET'])
def get_containers_status():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    return handle_get_container_status()

if __name__ == "__main__":
    init()
    api.run(host="0.0.0.0", port = 42055)