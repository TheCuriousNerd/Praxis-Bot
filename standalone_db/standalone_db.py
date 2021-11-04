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

import asyncio
from logging import exception

import time

import flask
from flask import Flask, request, after_this_request
import sqlalchemy as db

import requests

import credentials

import config

import os
import bot_functions.praxis_logging as praxis_logging
from bot_functions import utilities_db as db_utility

praxis_logger_obj = praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

credentials_manager = credentials.Credentials_Module()
credentials_manager.load_credentials()
dbCert: credentials.DB_Credential = credentials_manager.find_Credential(credentials.DB_Credential, config.credentialsNickname)

user = dbCert.username
password = dbCert.password
hostName = dbCert.ipAddress
databaseName = dbCert.databaseName
connectionString = "postgresql://%s:%s@%s/%s" % (user, password, hostName, databaseName)

db_obj = db_utility.Praxis_DB_Connection(autoConnect=True)

api = flask.Flask(__name__)
# enable/disable this to get web pages of crashes returned
api.config["DEBUG"] = False

def test_init():
    global db_obj
    db_obj = db_utility.Praxis_DB_Connection(autoConnect=True)

    try:
        db_obj.execQuery(
            'DROP TABLE users'
        )
    except:
        praxis_logger_obj.log("Couldn't Drop it")

    try:
        db_obj.execQuery(
        'CREATE TABLE users ('
        'id SERIAL, '
        'name TEXT);'
    )
    except:
        praxis_logger_obj.log("Couldn't Make it")

    try:
        db_obj.execQuery(
            'DELETE FROM users WHERE id = 1;'
        )
    except:
        pass


    try:
        for x in range(10):
            db_obj.execQuery(
            'INSERT INTO users '
            '(name) '
            'VALUES (\'Test Name\');'
            )
    except:
        pass

    try:
        results = db_obj.execQuery(
            'SELECT * FROM '
            'users;'
        )

        for item in results:
            praxis_logger_obj.log(item)
    except:
        pass


def init():
    #global db_obj
    #db_obj = db_utility.Praxis_DB_Connection(autoConnect=True)
    setup_basic_data()
    setup_basicCommands()
    create_basicCommands()

    createExternalAPI_Tables()


# Basic Data Table Functions

def setup_basic_data():
    #global db_obj
    try:
        #db_obj.execQuery('DROP TABLE basic_key_vars')
        if db_obj.doesTableExist("basic_key_vars") == False:
            query = (
                'CREATE TABLE basic_key_vars ('
                'id SERIAL, '
                'key TEXT, '
                'var TEXT);'
                )
            print(query)
            db_obj.execQuery(query)
            praxis_logger_obj.log("[Table Created]: (basic_key_vars)")
    except:
        praxis_logger_obj.log("[Table Creation Failed or Already Exists]: (basic_key_vars)")

def get_basic_data(key):
    #global db_obj
    try:
        returns = ""
        query = (
            'SELECT * FROM '
            'basic_key_vars '
            'WHERE key = \'%s\';' % (key)
            )
        print(query)
        results = db_obj.execQuery(query)
        for item in results:
            returns = returns + str(item) + " "
            praxis_logger_obj.log(item)
        return returns
    except:
        return False

def set_basic_data(key, var):
    #global db_obj
    try:
        query = (
            'INSERT INTO basic_key_vars '
            '(key, var) '
            'VALUES (\'%s\',\'%s\');' % (key, var)
            )
        print(query)
        db_obj.execQuery(query)
        return 'Insertion Done'
    except:
        return 'Insertion Failed'


# Basic Commands Table Functions

def setup_basicCommands():
    #global db_obj
    #db_obj = db_utility.Praxis_DB_Connection(autoConnect=True)
    try:
        #db_obj.execQuery('DROP TABLE command_responses_v0')
        if db_obj.doesTableExist("command_responses_v0") == False:
            print("Making setup_basicCommands Table")
            query = (
                'CREATE TABLE command_responses_v0 ('
                'id SERIAL, '
                'command TEXT, '
                'response TEXT);'
                )
            #print(query)
            results = db_obj.execQuery(query)
            praxis_logger_obj.log("[Table Created]: (command_responses_v0)")
    except exception:
        praxis_logger_obj.log("[Table Creation Failed or Already Exists]: (command_responses_v0)")
        praxis_logger_obj.log(exception)

def create_basicCommands():
    print("Creating Basic Commands for command_responses_v0")
    create_basicCommand("!testerino_v3", "A Testerino is Detected $(testFunction $(#*))")
    create_basicCommand("!math", "$(#*) = $(math $(#*))")
    create_basicCommand("!presentdaypresenttime", "The current date and time is: $(date %Y-%m-%d %H:%M:%S)")
    create_basicCommand("!curdaytime", "The current date and time is: $(date $(#*))")
    create_basicCommand("!convertunit", "$(#0) $(#1) = $(math_unitConversion $(#*)) $(#2)")

    create_basicCommand("!cryptoprice", "The current price of $(#0) against $(#1) is $(getCryptoPrice $(#0) $(#1))")

    #create_basicCommand("!chyron", "$(chyron $(#*))")
    #create_basicCommand("!roll", "$(roll $(#*))")
    #create_basicCommand("!lights", "$(lights $(#*))")
    #create_basicCommand("!text", "$(text $(#*))")
    #create_basicCommand("!tts", "$(tts $(#*))")

def create_basicCommand(commandName:str, commandReponse:str):
    #global db_obj
    #db_obj = db_utility.Praxis_DB_Connection(autoConnect=True)
    result = db_obj.doesItemExist("command_responses_v0", "command", commandName)
    if (db_obj.doesTableExist("command_responses_v0") == True) and (result == False):
        praxis_logger_obj.log("Creating Basic Command:")
        praxis_logger_obj.log(commandName)
        print("Creating Basic Command:")
        print(commandName)
        query = (
                'INSERT INTO command_responses_v0 '
                '(command, response) '
                'VALUES (\'%s\',\'%s\');' % (commandName, commandReponse)
                )
        #print(query)
        results = db_obj.execQuery(query)
        #print(str(results))

# External Api Functions
def createExternalAPI_Tables():
    #global db_obj
    #db_obj = db_utility.Praxis_DB_Connection(autoConnect=True)
    try:
        if db_obj.doesTableExist("external_api_v0") == False:
            query = (
                'CREATE TABLE external_api_v0 ('
                'id SERIAL, '
                'name TEXT, '
                'url TEXT, '
                'method TEXT, '
                'parameters TEXT, '
                'response TEXT, '
                'time TEXT);'
                )
            print(query)
            db_obj.execQuery(query)
            praxis_logger_obj.log("[Table Created]: (external_api_v0)")
    except:
        praxis_logger_obj.log("[Table Creation Failed or Already Exists]: (external_api_v0)")



# API Stuff

@api.route('/api/v1/get_data/basic_key_vars', methods=['GET'])
def get_data():
    if 'key_name' not in request.args:
        return flask.make_response('{\"text\":"Argument \'key_name\' not in request"}', 400)
    result = get_basic_data(request.args['key_name'])
    return flask.make_response("{\"message\":\"%s\"}" % result, 200, {"Content-Type": "application/json"})

@api.route('/api/v1/set_data/basic_key_vars', methods=['GET'])
def set_data():
    if 'key_name' not in request.args:
        return flask.make_response('{\"text\":"Argument \'key_name\' not in request"}', 400)
    if 'var_string' not in request.args:
        return flask.make_response('{\"text\":"Argument \'var_string\' not in request"}', 400)
    result = set_basic_data(request.args['key_name'], request.args['var_string'])
    return flask.make_response("{\"message\":\"%s\"}" % result, 200, {"Content-Type": "application/json"})

@api.route('/', methods=['GET'])
def command_check():
    return flask.make_response('BOO', 200)

if __name__ == "__main__":
    time.sleep(5)
    init()
    api.run(host='0.0.0.0', port=42002)
