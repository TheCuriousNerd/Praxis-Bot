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

from ..bot_functions import obsWebSocket as obsWebSocket

import os
from ..bot_functions import praxis_logging as praxis_logging
praxis_logger_obj = praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

api = flask.Flask(__name__)
# enable/disable this to get web pages of crashes returned
api.config["DEBUG"] = False

possibleRequests = []

def init():
    possibleRequests = obsWebSocket.getRequests()
    for r in possibleRequests:
        print("requestname: "+r)
    #obsWebSocket.makeRequest("ToggleStudioMode", {'source':'tinycam', 'render':'True'})
    #obsWebSocket.makeRequest("SetSourceRender", data={'source':"tinycam", 'render': False, 'scene-name':"Cam feed (main) INFOBOX"})
    #obsWebSocket.makeRequest("SetSourceRender", data={'source':"tinycam", 'render': True, 'scene-name':"Cam feed (main) INFOBOX"})

    #obsWebSocket.listenForData()

def do_request(requestName, data):
    if requestName in possibleRequests:
        obsWebSocket.makeRequest(requestName, data)

@api.route('/api/v1/obs/websocket/makeRequest', methods=['GET'])
def makeRequest():
    if 'request_name' not in request.args:
        return flask.make_response('{\"text\":"Argument \'request_name\' not in request"}', 400)
    if 'request_data' not in request.args:
        data = None
    else:
        data = request.args['request_data']
    #possibleRequests = obsWebSocket.getRequests()
    do_request(request.args['request_name'], data)

if __name__ == "__main__":
    init()
    api.run(host='0.0.0.0', port=12310)