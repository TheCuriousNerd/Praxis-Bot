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
from flask import request

from json import loads
from urllib.parse import urlencode

import requests

import os
import bot_functions.praxis_logging as praxis_logging
praxis_logger_obj = praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

api = flask.Flask(__name__)
# enable/disable this to get web pages of crashes returned
api.config["DEBUG"] = False

def init():
    praxis_logger_obj.log("init stuff")

def send_text(tts_sender, tts_text):

    #Play Text
    params = urlencode({'tts_sender': tts_sender, 'tts_text': tts_text})

    url = "http://192.168.191.126:40085/api/v1/tts/speech?%s" % params
    resp = requests.get(url)
    if resp.status_code == 200:
            print("Got the following message: %s" % resp.text)
            #data = loads(resp.text)
            #msg = data['message']
            #if msg is not None:
                #pass
            #else:
            # todo handle failed requests
                #pass

    #return None
    return flask.make_response('', 200)

@api.route('/api/v1/tts/send_text', methods=['GET'])
def tts_send_text():
    if 'tts_sender' not in request.args:
        tts_sender = ""
    if 'tts_text' not in request.args:
        return flask.make_response('{\"text\":"Argument \'tts_text\' not in request"}', 400)

    return send_text(request.args['tts_sender'], request.args['tts_text'])

if __name__ == '__main__':
    #send_text("","Blah Blah Blah")
    #init()
    api.run(host='0.0.0.0', port=42064)