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


if __name__ == "__main__":
    time.sleep(5)
    test_init()
