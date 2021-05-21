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
from enum import Enum
from os import F_OK
from ..bot_functions import tempText_Module
import time
from .. import config as config

import flask
from flask import Flask, request, after_this_request

import credentials

from ..commands import loader as command_loader
from ..commands.command_base import AbstractCommand

from ..bot_functions.cooldowns import Cooldown_Module

from ..bot_functions import utilities_script as utility

from ..bot_functions import chyron_module
from ..bot_functions import timers_module

import random

import json
import base64

import event_logs.event_log_Module

import os
from ..bot_functions import praxis_logging as praxis_logging
praxis_logger_obj = bot_functions.praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

api:Flask = Flask(__name__)
api.config["DEBUG"] = True

logging_module = event_logs.event_log_Module.Event_Log_Module()

def init():
    print("starting up... ",)
    logging_module.main()

def add_event(eventName, eventTime, eventType, eventSender, eventData):
    logging_module.make_event(eventName, eventTime, eventType, eventSender, eventData)
    return flask.make_response("{\"message\":\"%s\"}" % None, 200, {"Content-Type": "application/json"})

def get_events():
    #returnedData = logging_module.get_recent_logs(50)
    try:
        masterDic = {}
        newDic = {}
        counter = 0
        for event in logging_module.Event_Log_List:
            #praxis_logger_obj.log("get event history debug thing: "+ str(event))
            #recentLog = self.Event_Log_List[-x]
            newDic['eventName'] = str(event.eventName)
            newDic['eventTime'] = str(event.eventTime)
            newDic['eventType'] = str(event.eventType)
            newDic['eventSender'] = str(event.eventSender)
            newDic['eventData'] = str(event.eventData)
            masterDic[str(counter)] = newDic
            counter = counter + 1
            newDic = {}
    except:
        masterDic = {}
    #returnedData = [""]
    #praxis_logger_obj.log("\nGotten Events" + str(masterDic))
    #print("\nGotten Events" + masterDic)
    payload = json.dumps(masterDic)
    payload = base64.b64encode(str.encode(payload))

    return flask.make_response("{\"message\":\"%s\"}" % payload.decode(), 200, {"Content-Type": "application/json"})

def reRunEvent_handler(eventName, eventTime, eventType, eventSender, eventData):
    attempt_Event_Rerun(eventName, eventTime, eventType, eventSender, eventData)
    return flask.make_response("{\"message\":\"%s\"}" % 'rerunning event....', 200, {"Content-Type": "application/json"})

def attempt_Event_Rerun(eventName, eventTime, eventType, eventSender, eventData):
    returnString = ""
    try:
        return flask.make_response("{\"message\":\"%s\"}" % returnString, 200, {"Content-Type": "application/json"})
    except:
        returnString = "Something Went Wrong!"
        return flask.make_response("{\"message\":\"%s\"}" % returnString, 200, {"Content-Type": "application/json"})

@api.route('/')
def bot_StatusIcon():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    return flask.make_response('Hello There', 200)

@api.route('/api/v1/event_log/status')
def bot_status():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    return flask.make_response('EventLog Service: OK', 200)


@api.route('/api/v1/event_log/add_event')
def add_event_log():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    if 'event_name' not in request.args:
        return flask.make_response('{\"text\":"Argument \'event_name\' not in request"}', 400)
    if 'event_time' not in request.args:
        return flask.make_response('{\"text\":"Argument \'event_time\' not in request"}', 400)
    if 'event_type' not in request.args:
        return flask.make_response('{\"text\":"Argument \'event_type\' not in request"}', 400)
    if 'eventSender' not in request.args:
        return flask.make_response('{\"text\":"Argument \'eventSender\' not in request"}', 400)
    if 'event_data' not in request.args:
        return flask.make_response('{\"text\":"Argument \'event_data\' not in request"}', 400)

    return add_event(request.args['event_name'], request.args['event_time'], request.args['event_type'], request.args['eventSender'], request.args['event_data'],)

@api.route('/api/v1/event_log/get_events')
def get_event_log():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    if 'request_data' not in request.args:
        requestData = 50
    return get_events()

@api.route('/api/v1/event_log/reRunEvent')
def reRunEvent():
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

    return reRunEvent_handler(request.args['eventName'], sentTime, request.args['eventType'], request.args['eventSender'], request.args['eventData'])



if __name__ == "__main__":
    init()
    api.run(host="0.0.0.0", port = 12308)