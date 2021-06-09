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

import time

import flask
import sqlalchemy as db

import os
import bot_functions.praxis_logging as praxis_logging
praxis_logger_obj = praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

user = "PRAXIS_BOT"
password = "PraxisPraxisPraxis"
hostName = "standalone_db_main"
databaseName = "PRAXIS_BOT_DB"
connectionString ="postgresql://%s:%s@%s/%s" % (user, password, hostName, databaseName)

dbConnection = None

api = flask.Flask(__name__)
# enable/disable this to get web pages of crashes returned
api.config["DEBUG"] = False

def test_init():
    global dbConnection
    dbConnection = db.create_engine(connectionString)

    try:
        dbConnection.execute(
            'DROP TABLE users'
        )
    except:
        praxis_logger_obj.log("Couldn't Drop it")

    try:
        dbConnection.execute(
        'CREATE TABLE users ('
        'id SERIAL, '
        'name TEXT);'
    )
    except:
        praxis_logger_obj.log("Couldn't Make it")

    try:
        dbConnection.execute(
            'DELETE FROM users WHERE id = 1;'
        )
    except:
        pass


    try:
        for x in range(10):
            dbConnection.execute(
            'INSERT INTO users '
            '(name) '
            'VALUES (\'Test Name\');'
            )
    except:
        pass

    try:
        results = dbConnection.execute(
            'SELECT * FROM '
            'users;'
        )

        for item in results:
            praxis_logger_obj.log(item)
    except:
        pass


def init():
    global dbConnection
    dbConnection = db.create_engine(connectionString)
    try:
        dbConnection.execute(
            'DROP TABLE basic_key_vars'
        )
        praxis_logger_obj.log("[Dropped]: (basic_key_vars)")
    except:
        praxis_logger_obj.log("[Couldn't Drop it]: (basic_key_vars)")
    try:
        dbConnection.execute(
        'CREATE TABLE basic_key_vars ('
        'id SERIAL, '
        'key TEXT, '
        'var TEXT);'
        )
        praxis_logger_obj.log("[Table Created]: (basic_key_vars)")
    except:
        praxis_logger_obj.log("[Table Creation Failed or Already Exists]: (basic_key_vars)")

def does_basic_key_exist(key):
    global dbConnection
    try:
        returns = ""
        results = dbConnection.execute(
        'SELECT * FROM '
        'basic_key_vars '
        'WHERE key = \'%s\';' % (key)
        )
        for item in results:
            returns = returns + str(item) + " "
            praxis_logger_obj.log(item)
        return returns
    except:
        return False

def set_basic_data(key, var):
    global dbConnection
    try:
        dbConnection.execute(
        'INSERT INTO basic_key_vars '
        '(key, var) '
        'VALUES (\'%s\',\'%s\');' % (key, var)
        )
        return 'Insertion Done'
    except:
        return 'Insertion Failed'

@api.route('/api/v1/get_data/<key_name>', methods=['GET'])
def get_data(key_name):
    result = does_basic_key_exist(key_name)
    return flask.make_response(str(result), 200)

@api.route('/api/v1/set_data/<key_name>/<var_string>', methods=['GET'])
def set_data(key_name, var_string):
    result = set_basic_data(key_name, var_string)
    return flask.make_response(str(result), 200)

@api.route('/', methods=['GET'])
def command_check():
    return flask.make_response('BOO', 200)

if __name__ == "__main__":
    time.sleep(5)
    init()
    api.run(host='0.0.0.0', port=42002)
