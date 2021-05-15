# The main repository of Praxis_Bot can be found at: <https://github.com/TheCuriousNerd/Praxis_Bot>.
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
import tempText_Module
import time
import config as config

import flask
from flask import Flask, request, after_this_request

import credentials

import commands.loader as command_loader
from commands.command_base import AbstractCommand

from cooldowns import Cooldown_Module

import utilities_script as utility

import chyron_module
import timers_module

import random

import os
import praxis_logging
praxis_logger_obj = praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

api:Flask = Flask(__name__)
api.config["DEBUG"] = True

class Module_InfoLookup():
    def __init__(self):
        super().__init__()


def init():
    print("starting up... ",)

@api.route('/')
def bot_StatusIcon():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    return flask.make_response('Client Service: OK', 200)

if __name__ == "__main__":
    init()
    api.run(host="0.0.0.0", port = 42063)