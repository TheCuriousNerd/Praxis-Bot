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

import credentials

import config

import twitchAPI
from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.types import AuthScope
from twitchAPI.oauth import UserAuthenticator
from pprint import pprint
from uuid import UUID

import json
import bot_functions.utilities_script as utility
import os

class Twitch_Credential_Maker():
    def __init__(self):
        super().__init__()
        self.credential : credentials.Twitch_Credential()
        self.twitch : Twitch()
        self.target_scope = [AuthScope.WHISPERS_READ, AuthScope.CHANNEL_READ_REDEMPTIONS, AuthScope.BITS_READ, AuthScope.CHANNEL_READ_SUBSCRIPTIONS]

    def get_tokens(self):
        self.twitch.authenticate_app(self.target_scope)
        for scope_ in self.target_scope:
            print(scope_)
        auth = UserAuthenticator(self.twitch, self.target_scope, force_verify=True)
        token, refresh_token = auth.authenticate()

        if token is not None: print("found token")
        if refresh_token is not None: print("found refresh_token\n")
        print("token: ", token)
        print("refresh_token: ", refresh_token)
        print("")
        return token, refresh_token

    def updateCredentialsFile(self, token, refreshToken):
        dir = utility.get_dir("credentials")
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        relative_path = "credentials/twitch.json"
        real_file_path = os.path.join(script_dir, relative_path)

        with open(real_file_path, 'r') as cred_r:
            data = json.load(cred_r)
            data['pubsub_AccessToken'] = token
            data['pubsub_RefreshToken'] = refreshToken

        os.remove(real_file_path)
        with open(real_file_path, 'w') as cred_w:
            json.dump(data, cred_w, indent=2)




if __name__ == "__main__":
    testModule = Twitch_Credential_Maker()

    credentials_manager = credentials.Credentials_Module()
    credentials_manager.load_credentials()
    testModule.credential = credentials_manager.find_Twitch_Credential(config.credentialsNickname)
    testModule.twitch = Twitch(testModule.credential.pubsub_client_id, testModule.credential.pubsub_secret)
    #pprint(testModule.twitch.get_users(logins=['thecuriousnerd']))

    token, refreshToken = testModule.get_tokens()
    print("Update credentials file? (y/n)")
    response = input()
    if "y" in response.lower():
        testModule.updateCredentialsFile(token, refreshToken)
    print("Ready to close")
    input()