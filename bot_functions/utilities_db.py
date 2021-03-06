# The main repository of Praxis Bot can be found at: <https://github.com/TheCuriousNerd/Praxis-Bot>.
# Copyright (C) 2021

# Author Info Examples:
#   Name / Email / Website
#       Twitter / Twitch / Youtube / Github

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

import time
import datetime
from logging import exception
import sqlalchemy as db

import credentials
import config
import os
class Praxis_DB_Connection():
    def __init__(self, autoConnect:bool=False):
        super().__init__()
        self.credentials_manager = credentials.Credentials_Module()
        self.credentials_manager.load_credentials()
        self.dbCert: credentials.DB_Credential = self.credentials_manager.find_Credential(credentials.DB_Credential, config.credentialsNickname)

        #self.connectionString = "postgresql://%s:%s@%s/%s" % (self.dbCert.username, self.dbCert.password, self.dbCert.ipAddress, self.dbCert.databaseName)
        self.connectionString = "postgresql://%s:%s@%s/%s" % (self.dbCert.username, self.dbCert.password, self.dbCert.ipAddress, self.dbCert.databaseName)

        self.dbConnection:db.engine.base.Engine = None
        if autoConnect == True:
            if not os.getenv("ISDOCKER"):
                self.startLocalConnection()
            else:
                self.startConnection()

    def startConnection(self):
        print("starting engine with: \n" + self.connectionString)
        self.dbConnection = db.create_engine(self.connectionString)

    def startLocalConnection(self):
        self.connectionString = "postgresql://%s:%s@%s/%s" % (self.dbCert.username, self.dbCert.password, "127.0.0.1", self.dbCert.databaseName)
        self.startConnection()

    def closeConnection(self):
        self.dbConnection.dispose()
        self.dbConnection = None

    def selfAutoStart(self):
        if self.dbConnection is None:
            print("Auto Starting Connection to DB")
            self.startConnection()

    def doesTableExist(self, tableName):
        try:
            self.selfAutoStart()
            query = "SELECT to_regclass('%s');" % tableName
            result = self.dbConnection.execute(query)
            for r in result:
                if r[0] == tableName:
                    self.closeConnection()
                    return True
            self.closeConnection()
            return False

        except:
            print("[Praxis_DB_Connection] query error")
            return False

    def doesItemExist(self, tableName, columnName, item):
        try:
            print("Searching for item")
            print(item)
            self.selfAutoStart()
            query = "SELECT * FROM %s WHERE %s = '%s';" % (tableName, columnName, item)
            try:
                result = self.dbConnection.execute(query)
            except Exception as e:
                print("[Praxis_DB_Connection] query error while looking for item")
                print(e)
                return False
            print(result)
            for r in result:
                print(r)
                if r[1] == item:
                    print("Found the item in DB")
                    self.closeConnection()
                    return True
            print("Did not find the item in DB")
            self.closeConnection()
            return False
        except:
            print("[Praxis_DB_Connection] query error")
            return False

    def deleteItems(self, tableName, columnName, item):
        try:
            self.selfAutoStart()
            query = "DELETE FROM %s WHERE %s = \'%s\';" % (tableName, columnName, item)
            self.dbConnection.execute(query)
            self.closeConnection()
            return True
        except:
            print("[Praxis_DB_Connection] query deletion error")
            return False

    def insertItem(self, tableName, columnName, item):
        try:
            self.selfAutoStart()
            columns = ", ".join(columnName)
            items = "', '".join(item)
            items = "'%s'" % items
            query = "INSERT INTO %s (%s) VALUES (%s);" % (tableName, columns, items)
            self.dbConnection.execute(query)
            self.closeConnection()
            return True
        except:
            print("[Praxis_DB_Connection] query insertion error")
            return False

    def updateItems(self, tableName, columnName, item, newItem_columnName, newItem):
        try:
            self.selfAutoStart()
            query = "UPDATE %s SET %s = '%s' WHERE %s = '%s';" % (tableName, newItem_columnName, newItem, columnName, item)
            self.dbConnection.execute(query)
            self.closeConnection()
            return True
        except Exception as e:
            print("[Praxis_DB_Connection] query update item row error")
            return None

    def getItemRow(self, tableName, columnName, item):
        try:
            self.selfAutoStart()
            query = "SELECT * FROM %s WHERE %s = '%s';" % (tableName, columnName, item)
            result = self.dbConnection.execute(query)
            print(result)
            self.closeConnection()
            for r in result:
                return r
        except Exception as e:
            print("[Praxis_DB_Connection] get query row error")
            print(str(e))
            return None

    def addAPI_Call(self, APIname, url, method, parameters, response, timeStamp):
        try:
            self.selfAutoStart()
            query = "INSERT INTO external_api_v0 (name, url, method, parameters, response, time) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (APIname, url, method, parameters, response, str(timeStamp))
            result = self.dbConnection.execute(query)
            self.closeConnection()
            return True
        except:
            print("[Praxis_DB_Connection] query error")

    def shouldICallAPI(self, APIname, seconds):
        try:
            self.selfAutoStart()
            query = "SELECT * FROM external_api_v0 WHERE name = '%s';" % APIname
            result = self.dbConnection.execute(query)
            results = None
            for r in result:
                results = r
            lastCalled = float(results[6])
            currentTime = time.time()
            self.closeConnection()
            return (currentTime - lastCalled) > seconds
        except:
            print("[Praxis_DB_Connection] query error")
            return False

    def getAPI_Call(self, APIname):
        try:
            self.selfAutoStart()
            query = "SELECT * FROM external_api_v0 WHERE name = '%s';" % APIname
            result = self.dbConnection.execute(query)
            results = None
            for r in result:
                    #praxis_logger_obj.log("query results:")
                    #praxis_logger_obj.log(r)
                    results = r
            self.closeConnection()
            return results
        except:
            print("[Praxis_DB_Connection] query error")
            return None

    def getTasksFromQueue(self, targetSystem):
        try:
            self.selfAutoStart()
            query = "SELECT * FROM task_queue_v0 WHERE target_standalone_system = \'%s\';" % (targetSystem)
            result = self.dbConnection.execute(query)
            results = []
            for r in result:
                results.append(r)
            self.closeConnection()
            return results
        except:
            print("[Praxis_DB_Connection] get query task error")
            return None

    def add_taskToQueue(self, target_standalone_system:str, name:str, time:str, command:str, parameters:str, bonus_data:str):
        try:
            self.selfAutoStart()
            query = (
            'INSERT INTO task_queue_v0 '
            '(target_standalone_system, name, time, command, parameters, bonus_data) '
            'VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' % (target_standalone_system, name, time, command, parameters, bonus_data)
            )
            result = self.dbConnection.execute(query)
            return True
        except:
            print("[Praxis_DB_Connection] add query task error")
            self.closeConnection()
            return None

    def get_chyronString(self, chyronName = ""):
        try:
            self.selfAutoStart()
            query = "SELECT * FROM home_chyron_entry ORDER BY id ASC"
            result = self.dbConnection.execute(query)
            results = []
            for r in result:
                results.append(r)
            self.closeConnection()
            return results
        except:
            print("[Praxis_DB_Connection] get query chyron error")
            return "None"


    def execQuery(self, query):
        try:
            self.selfAutoStart()
            result = self.dbConnection.execute(query)
            self.closeConnection()
            return result
        except Exception as e:
            print("[Praxis_DB_Connection] query error")
            return e


    # OLD DO NOT USE FURTHER it returns the oldest row
    import bot_functions.praxis_logging as praxis_logging
    def execQuery_old(self, query, praxis_logger_obj:praxis_logging.praxis_logger = praxis_logging.praxis_logger()):
        try:
            self.selfAutoStart()
            #praxis_logger_obj.log("query:")
            #praxis_logger_obj.log(query)
            print("query:")
            print(query)
            results = None
            try:
                results = self.dbConnection.execute(query)
                for r in results:
                    #praxis_logger_obj.log("query results:")
                    #praxis_logger_obj.log(r)
                    results = r
            except:
                results = None

            print("execQuery results:")
            print(results)
            #praxis_logger_obj.log("execQuery results:")
            #praxis_logger_obj.log(results)
            self.closeConnection()
            return results
        except Exception as e:
            print("[Praxis_DB_Connection] query error")
            print(e)
            return e