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

import threading
import config
from bot_functions import utilities_script as utilities
import flask
from flask import Flask

import time

import requests
from urllib.parse import urlencode

api:Flask = Flask(__name__)
api.config["DEBUG"] = False



def main():
    pass
    thread_updater = threading.Thread(target=core_Status_Updater)
    thread_updater.start()
    #thread_updater.join()
    thread = threading.Thread(target=Networking_Module_Main)
    thread.start()
    # thread.join()
    # print("API is running on port " + str(config.standalone_ping_port))

def core_Status_Updater():
    loopBool = True
    while loopBool:
        try:
            print("Pinging Core")
            params = urlencode(
                {'container_name': utilities.getContainerName()})
            print("params made")
            url = "http://%s:%s/api/v1/containers/container/ping?%s" % (
                config.standalone_core_manager_address[0].get("ip"),
                config.standalone_core_manager_address[0].get("port"),
                params)
            print("url made")
            resp = requests.get(url)
            print("resp made")
            time.sleep(config.standalone_ping_interval)
        except:
            print("Error in core_Status_Updater")
            time.sleep(config.standalone_ping_interval)
            #loopBool = False
    return None

def Networking_Module_Main():
    api.run(host="0.0.0.0", port = config.standalone_ping_port)

@api.route('/api/v1/ping')
def ping():
    #return "pong"
    return flask.make_response("{\"message\":\"%s\"}" % "pong", 200, {"Content-Type": "application/json"})


if __name__ == "__main__":
    main()