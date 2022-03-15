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

import config
from bot_functions import utilities_script as utilities
import requests

import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass

class Container_Stats_Lookup:
    def __init__(self):
        super().__init__()
        # standalone_core_manager
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
        self.containerList = [
            "standalone-core-manager",
            "standalone-eventlog",
            "standalone-user-client",
            "standalone-websource",
            "standalone-lights",
            "standalone-tts-core",
            "standalone-channelrewards",
            "standalone-command",
            "standalone-discord-script",
            "standalone-twitch-script",
            "standalone-twitch-pubsub"
        ]
        self.containerAddresses = {
            "standalone-core-manager": config.standalone_core_manager_address,
            "standalone-eventlog": config.standalone_eventlog_address,
            "standalone-user-client": config.standalone_user_client_address,
            "standalone-websource": config.standalone_websource_address,
            "standalone-lights": config.standalone_lights_address,
            "standalone-tts-core": config.standalone_tts_core_address,
            "standalone-channelrewards": config.standalone_channelrewards_address,
            "standalone-command": config.standalone_command_address,
            "standalone-discord-script": config.standalone_discord_script_address,
            "standalone-twitch-script": config.standalone_twitch_script_address,
            "standalone-twitch-pubsub": config.standalone_twitch_pubsub_address
        }
        self.containerLastPingTime = {}
        self.current_stats = {}

    def init(self):
        for name in self.containerList:
            self.current_stats[name] = "No Ping Yet"
            self.containerLastPingTime[name] = 0
        return self.current_stats

    def main(self):
        for name in self.containerList:
            if name != "standalone-core-manager":
                self.current_stats[name] = self.get_container_stats(self.containerAddresses[name])
        return self.current_stats

    # @contextmanager
    # def time_limit(self, seconds):
    #     def signal_handler(sig, frame):
    #         raise TimeoutException("Timed out!")
    #     signal.signal(signal.SIGALRM, signal_handler)
    #     signal.alarm(seconds)
    #     try:
    #         yield
    #     finally:
    #         signal.alarm(0)

    def get_container_stats(self, targetContainer):
        try:
            url = "http://%s:%s/api/v1/ping" % (targetContainer[0].get("ip"), config.standalone_ping_port)

            resp = requests.get(url, verify=False)
            return "Online"
        except TimeoutException:
            return "Lookup Error"
        except:
            return "Unknown"

if __name__ == "__main__":
    container_stats_lookup = Container_Stats_Lookup()
    container_stats_lookup.main()