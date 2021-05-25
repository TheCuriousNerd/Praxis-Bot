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

import config as config

import pandas as pd
from sqlalchemy import create_engine


class db_module():
    def __init__(self):
        super().__init__()
        self.dbCredential: credentials.DB_Credential
        self.currentWorkingDB: str
        self.engine = None

    def setup_engine(self, credential: credentials.DB_Credential = None):
        createEngine = True
        if credential is None:
            if self.dbCredential is None:
                createEngine = False
            else:
                credential = self.dbCredential

        if createEngine:
            self.engine = create_engine(credential.engine_url)
            self.currentWorkingDB = credential.databaseName
            print("SQL Engine Created")

    def create_table(self, tableName: str = ""):
        pass

    def does_table_exist(self, tableName: str = ""):
        pass

    def delete_table(self, tableName: str = ""):
        pass

    # This was a old function used prior to the creation of this class. I need to remake it.
#    def get_data_old(self, tableName: str = "", key: str = ""):
#        table = '_channel_commands'
#        table = tableName
#
#        df = pd.read_sql_query('SELECT * FROM ' + table, engine)
#        stmt = "trigger == '" + key + "'"
#        temp = df.query(stmt)
#        result = temp.get("response")
#
#        # print(result)
#        i = len(temp.index.values)
#
#        if i == 1:
#            output = result[temp.index.values[0]]
#            pass
#        else:
#            output = "$$None$$"
#        return output

    def get_data(self, tableName: str = "", key: str = ""):
        pass

    def insert_data(self, tableName: str = "", param: str = ""):
        pass

    def edit_data(self, tableName: str = "", key: str = "", param: str = ""):
        pass

    def delete_data(self, tableName: str = "", key: str = ""):
        pass


if __name__ == "__main__":
    testModule = db_module()

    credentials_manager = credentials.Credentials_Module()
    credentials_manager.load_credentials()
    testModule.dbCredential = credentials_manager.find_DB_Credential(config.credentialsNickname)

    testModule.setup_engine()