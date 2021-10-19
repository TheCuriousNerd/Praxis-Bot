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

from logging import exception
import sqlalchemy as db

import credentials
import config
class Praxis_DB_Connection():
    def __init__(self, autoConnect:bool=False):
        super().__init__()
        self.credentials_manager = credentials.Credentials_Module()
        self.credentials_manager.load_credentials()
        self.dbCert: credentials.DB_Credential = self.credentials_manager.find_Credential(credentials.DB_Credential, config.credentialsNickname)

        #self.connectionString = "postgresql://%s:%s@%s/%s" % (self.dbCert.username, self.dbCert.password, self.dbCert.ipAddress, self.dbCert.databaseName)
        self.connectionString = "postgresql://%s:%s@%s/%s" % (self.dbCert.username, self.dbCert.password, self.dbCert.ipAddress, self.dbCert.databaseName)

        self.dbConnection = None
        if autoConnect == True:
            self.startConnection()

    def startConnection(self):
        print("starting engine with: \n" + self.connectionString)
        self.dbConnection = db.create_engine(self.connectionString)

    def closeConnection(self):
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
                    return True
            return False

        except:
            print("[Praxis_DB_Connection] query error")
            return False

    def doesItemExist(self, tableName, rowName, item):
        try:
            print("Searching for item")
            #self.selfAutoStart()
            query = "SELECT * FROM %s WHERE %s = '%s';" % (tableName, rowName, item)
            result = self.dbConnection.execute(query)
            print(result)
            for r in result:
                print(r)
                if r[1] == item:
                    print("Found the item in DB")
                    return True
            print("Did not find the item in DB")
            return False
        except:
            print("[Praxis_DB_Connection] query error")
            return False

    import bot_functions.praxis_logging as praxis_logging
    def execQuery(self, query, praxis_logger_obj:praxis_logging.praxis_logger = praxis_logging.praxis_logger()):
        try:
            #self.selfAutoStart()
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
            return results
        except Exception as e:
            print("[Praxis_DB_Connection] query error")
            print(e)
            return e