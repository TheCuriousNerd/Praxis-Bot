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
        print("Couldn't Drop it")

    try:
        dbConnection.execute(
        'CREATE TABLE users ('
        'id SERIAL, '
        'name TEXT);'
    )
    except:
        print("Couldn't Make it")

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
            print(item)
    except:
        pass


@api.route('/api/v1/', methods=['GET'])
def get_data():
    return flask.make_response('BOO', 200)

@api.route('/api/v1/', methods=['GET'])
def set_data():
    return flask.make_response('BOO', 200)

@api.route('/', methods=['GET'])
def command_check():
    return flask.make_response('BOO', 200)

if __name__ == "__main__":
    time.sleep(5)
    test_init()
    api.run(host='0.0.0.0', port=42002)
