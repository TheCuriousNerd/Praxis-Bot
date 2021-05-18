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



# I moved all the requirements into requirements.txt.
# you can install everything with pip install -r requirements.txt while you're in the directory

import sys
import time

import test_module

import user_module

import bot_functions.utilities_script as utility
import config as config

import credentials

import threading

testModule_: test_module.Test_Module
userModule_: user_module.User_Module

credentials_manager: credentials.Credentials_Module

def main(inputArg):
    args = utility.get_args(inputArg)


def test_module_init(dbCert, Empty):
    print("-init [TEST Module]")
    #testModule_.dbCredential = dbCert
    testModule_.main()

def user_module_init(dbCert, Empty):
    print("-init [USER Module]")
    userModule_.dbCredential = dbCert
    userModule_.main()

def thread_main():
    if utility.isRunningInDocker() == True:
        print("<[DOCKER Detected]>")
    if not config.skip_splashScreen:
        utility.splashScreen()
    global credentials_manager
    global testModule_
    global userModule_

    credentials_manager = credentials.Credentials_Module()

    testModule_ = test_module.Test_Module()
    userModule_ = user_module.User_Module()

    credentials_manager.load_credentials()
    dbCert: credentials.DB_Credential = credentials_manager.find_Credential(credentials.DB_Credential, config.credentialsNickname)

    threads = []
    if config.test_module == True:
        thread_ = threading.Thread(target=test_module_init, args=(dbCert, None))
        thread_.daemon = True
        threads.append(thread_)
        thread_.start()

    if config.user_module == True:
        if utility.isRunningInDocker() == False:
            config.user_module = False
            thread_ = threading.Thread(target=user_module_init, args=(dbCert, None))
            thread_.daemon = True
            threads.append(thread_)
            thread_.start()

    print("---Post Thread Creation Test---\n")
    for t in threads:
        t.join()

    print("---Point of no return---")
    if utility.isRunningInDocker() == False:
        input()



if __name__ == "__main__":
    thread_main()
