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
import os
from enum import Enum


class Credential(Enum):
    Twitch_Credential = 1
    Discord_Credential = 2
    DB_Credential = 3


class Twitch_Credential():
    # Username = Twitch Username
    # Helix ID = https://dev.twitch.tv/console/apps
    # Oauth = https://twitchapps.com/tmi/
    # V5 Client ID = https://twitchtokengenerator.com/
    def __init__(self, username, helix, oauth, v5_client, pubsub_client_id, pubsub_secret, pubsub_AccessToken, pubsub_RefreshToken):
        # super().__init__()
        self.username = username
        self.helix = helix
        self.oauth = oauth
        self.v5_client = v5_client
        self.pubsub_client_id = pubsub_client_id
        self.pubsub_secret = pubsub_secret
        self.pubsub_AccessToken = pubsub_AccessToken
        self.pubsub_RefreshToken = pubsub_RefreshToken


class Discord_Credential():
    # Discord Credentials explanations here.
    def __init__(self, nickname, token):
        # super().__init__()
        self.nickname = nickname
        self.token = token

class DB_Credential():
    def __init__(self, nickname, username, password, ipAddress, port, databaseName, engine_url):
        #super().__init__()
        self.nickname = nickname
        self.username = username
        self.password = password
        self.ipAddress = ipAddress
        self.port = port
        self.databaseName = databaseName
        self.engine_url = engine_url

    def create_engine_url(self):
        new_engine_url = "postgresql://%s:%s@%s/%s" % (self.username, self.password, self.ipAddress, self.databaseName)
        self.engine_url = new_engine_url
        return new_engine_url


class Credentials_Module():
    def __init__(self):
        super().__init__()
        self.Twitch_Credentials_List: list = []
        self.Discord_Credentials_List: list = []
        self.DB_Credentials_List: list = []

    def load_credentials(self):
        print("Loading credentials...")
        fileList = self.list_credential_files()
        for file in fileList:
            if file.lower().find("twitch") != -1:
                credential_loading_function = self.credentialLoadingFunctions.get(Credential.Twitch_Credential)
                output = credential_loading_function(self, file)
                self.Twitch_Credentials_List.append(output)
            if file.lower().find("discord") != -1:
                credential_loading_function = self.credentialLoadingFunctions.get(Credential.Discord_Credential)
                output = credential_loading_function(self, file)
                self.Discord_Credentials_List.append(output)
            if file.lower().find("db") != -1:
                credential_loading_function = self.credentialLoadingFunctions.get(Credential.DB_Credential)
                output = credential_loading_function(self, file)
                self.DB_Credentials_List.append(output)

    def list_credential_files(self):
        credentialPath = self.get_credentials_dir()
        fileList: list = []
        for dirName, subdirList, fileList in os.walk(credentialPath):
            break
        return fileList

    # Based on similar function in tts.py
    def get_credentials_dir(self):
        dir = os.path.join(os.getcwd(), "credentials")  # this is platform-agnostic
        if not os.path.exists(dir):
            os.mkdir(dir)
        return dir

    def load_Twitch_Credential(self, fileName: str):
        file_path = os.path.join(self.get_credentials_dir(), fileName)
        f = open(file_path)
        raw_json = json.loads(f.read())
        tobj = Twitch_Credential(**raw_json)
        return tobj

    def load_Discord_Credential(self, fileName: str):
        file_path = os.path.join(self.get_credentials_dir(), fileName)
        f = open(file_path)
        raw_json = json.loads(f.read())
        tobj = Discord_Credential(**raw_json)
        return tobj

    def load_DB_Credential(self, fileName: str):
        file_path = os.path.join(self.get_credentials_dir(), fileName)
        f = open(file_path)
        raw_json = json.loads(f.read())
        tobj = DB_Credential(**raw_json)
        return tobj

    def find_Credential(self, credentialType, searchParam: str):
        print("Searching for credential named: " + searchParam)
        if credentialType.__name__ == Twitch_Credential.__name__:
            print(".\{Twitch Credential Detected}")
            credential_search_function = self.credentialSearchFunctions.get(Credential.Twitch_Credential)
            output = credential_search_function(self, searchParam)
            return output
        elif credentialType.__name__ == Discord_Credential.__name__:
            print(".\{Discord Credential Detected}")
            credential_search_function = self.credentialSearchFunctions.get(Credential.Twitch_Credential)
            output = credential_search_function(self, searchParam)
            return output
        elif credentialType.__name__ == DB_Credential.__name__:
            print(".\{DB Credential Detected}")
            credential_search_function = self.credentialSearchFunctions.get(Credential.DB_Credential)
            output = credential_search_function(self, searchParam)
            return output
        else:
            print(".\{Something else Detected}")
            return None

    def find_Twitch_Credential(self, searchParam: str):
        print("Searching for Twitch Credential named: " + searchParam)
        foundSomething = False
        tempCert: Twitch_Credential = None
        for cert in self.Twitch_Credentials_List:
            if cert.username == searchParam:
                print("Twitch Credential Found: {" + cert.username + "}")
                tempCert = cert
                foundSomething = True
        if foundSomething:
            return tempCert
        else:
            return None

    def find_Discord_Credential(self, searchParam: str):
        print("Searching for Discord Credential named: " + searchParam)
        foundSomething = False
        tempCert: Discord_Credential = None
        for cert in self.Discord_Credentials_List:
            if cert.nickname == searchParam:
                print("Discord Credential Found: {" + cert.nickname + "}")
                tempCert = cert
                foundSomething = True
        if foundSomething:
            return tempCert
        else:
            return None

    def find_DB_Credential(self, searchParam: str):
        print("Searching for DB Credential named: " + searchParam)
        foundSomething = False
        tempCert: DB_Credential = None
        for cert in self.DB_Credentials_List:
            if cert.nickname == searchParam:
                print("DB Credential Found: {" + cert.nickname + "}")
                tempCert = cert
                foundSomething = True
        if foundSomething:
            return tempCert
        else:
            return None


    credentialLoadingFunctions = {  # this is a mapping of the Credential enum to function pointers
        Credential.Twitch_Credential: load_Twitch_Credential,
        Credential.Discord_Credential: load_Discord_Credential,
        Credential.DB_Credential: load_DB_Credential

    }
    credentialSearchFunctions = {  # this is a mapping of the Credential enum to function pointers
        Credential.Twitch_Credential: find_Twitch_Credential,
        Credential.Discord_Credential: find_Discord_Credential,
        Credential.DB_Credential: find_DB_Credential

    }

if __name__ == '__main__':
    creds = Credentials_Module()
    creds.load_credentials()

    creds.find_Credential(DB_Credential, "Praxis-Bot")
    creds.find_Credential(Twitch_Credential, "Praxis-Bot")


