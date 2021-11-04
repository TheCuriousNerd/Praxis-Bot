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
import requests
from json import dumps
from json import loads
import datetime

from bot_functions import utilities_db


class CryptoStats():
    def __init__(self):
        self.tokenRefreshTime = 60
        self.db = utilities_db.Praxis_DB_Connection()
        #self.db.connectionString = "postgresql://PRAXIS_BOT:PRAXISPRAXISPRAXIS@standalone_db_main/PRAXIS_BOT_DB"
        self.db.startConnection()
        self.lastAPI_Response = ""
        self.lastAPI_ResponseTime = None

    def getCryptoPrice(self, targetCrypto:str, cryptoToCompareAgainst:str):
        # Looks up most recent price of a token in db, if its older than 60 seconds, update it.

        #return str(self.getAPICallResultsFromDB())

        self.updateTokens()
        # for token in self.lastAPI_Response:
        #     print(token)
        #     print(type(token))
        searchSymbol = targetCrypto.upper() + cryptoToCompareAgainst.upper()
        for token in self.lastAPI_Response:
            #print(token)
            if token['symbol'] == searchSymbol:
                return str(token['price'])


    def updateTokens(self):
        self.getAPICallResultsFromDB()
        if self.lastAPI_ResponseTime is None:
            return self.refreshTokens()
        elif self.isTokenOlderThan(self.lastAPI_ResponseTime, self.tokenRefreshTime):
            return self.refreshTokens()

    def isTokenOlderThan(self, tokenTime, seconds):
        if tokenTime is None:
            return True
        else:
            return (time.time() - tokenTime) > seconds

    def refreshTokens(self):
        curPrices = self.get_currentPrice_binance()
        self.lastAPI_Response = curPrices
        self.lastAPI_ResponseTime = time.time()
        self.addAPICallToDB()
        return curPrices

    def addAPICallToDB(self):
        self.db.addAPI_Call("binance", "https://api.binance.com/api/v3/ticker/price", "", "", dumps(self.lastAPI_Response), str(self.lastAPI_ResponseTime))

    def getAPICallResultsFromDB(self):
        try:
            results = self.db.getAPI_Call("binance")
            self.lastAPI_Response = loads(results[5])
            self.lastAPI_ResponseTime = float(results[6])
        except:
            pass
        return results

    # def get_currentEthPrice(self):
    #     url = "https://api.etherscan.io/api?module=stats&action=ethprice"
    #     headers = {'User-Agent': 'Mozilla/5.0'}
    #     response = requests.get(url, headers=headers)
    #     data = loads(response.text)

    #     return data

    def get_currentPrice_binance(self):
        url = "https://api.binance.com/api/v3/ticker/price"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        data = loads(response.text)
        return data

    # def getEthAddressTokens(self, address):
    #     url = "https://api.etherscan.io/api?module=account&action=tokentx&address=" + address + "&startblock=0&endblock=999999999&sort=asc&apikey=YourApiKeyToken"
    #     headers = {'User-Agent': 'Mozilla/5.0'}
    #     response = requests.get(url, headers=headers)
    #     data = loads(response.text)

    #     return data['result']



if __name__ == "__main__":
    cs = CryptoStats()
    print(cs.getCryptoPrice("ETH", "USDT"))
