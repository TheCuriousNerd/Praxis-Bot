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

from ..bot_functions import tts as tts

import config
from ..bot_functions import utilities_script as utility

import os
from ..bot_functions import praxis_logging as praxis_logging
praxis_logger_obj = praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

api = flask.Flask(__name__)
# enable/disable this to get web pages of crashes returned
api.config["DEBUG"] = False

def init():
    praxis_logger_obj.log("init stuff")

def isTTS_URL_Check(message):
    isNotBlocked = True
    is_ttsEnabled = config.is_tts_Speaker_Enabled
    is_tts_URL_Allowed = not config.is_tts_URL_Blocked
    has_URL = False
    if utility.contains_url(message):
            has_URL = True

    if is_tts_URL_Allowed:
        if has_URL:
            has_URL = False
    if has_URL:
        isNotBlocked = False
    if not is_ttsEnabled:
        isNotBlocked = False

    return not isNotBlocked

def try_TTS(tts_sender, tts_text):
    text_to_say: str = "%s says, %s" % (tts_sender, tts_text)

    #tts.tts(str(text_to_say))
    #tts.tts(str(tts_text))
    if tts_sender == "":
        text_to_say = tts_text

    if isTTS_URL_Check(tts_text):
        if not utility.contains_slur(tts_sender):
            if not utility.contains_slur(text_to_say):
                tts.tts(str(text_to_say))

    return flask.make_response('', 200)

@api.route('/api/v1/tts/speech', methods=['GET'])
def tts_speech():
    if 'tts_sender' not in request.args:
        tts_sender = ""
    else:
        tts_sender = request.args['tts_sender']
    if 'tts_text' not in request.args:
        return flask.make_response('{\"text\":"Argument \'tts_text\' not in request"}', 400)

    return try_TTS(tts_sender, request.args['tts_text'])

if __name__ == '__main__':
    #init()
    api.run(host='0.0.0.0', port=40085)