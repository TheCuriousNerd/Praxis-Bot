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

import requests
from json import loads
import datetime

class CryptoStats():
    class Token():
        def __init__(self, name, symbol, balance, price, timestamp):
            self.name = name
            self.symbol = symbol
            self.balance = balance
            self.price = price
            self.time = timestamp

    def __init__(self):
        self.tokens = []
        self.tokenRefreshTime = 60
        self.updateTokens()

    def updateTokens(self):
        self.tokens = []
        self.tokens.append(CryptoStats.Token("ETH", "ETH", 0, self.get_currentEthPrice(), datetime.datetime.now()))
        self.tokens.append(CryptoStats.Token("BTC", "BTC", 0, self.get_currentBtcPrice(), datetime.datetime.now()))

    def isTokenOlderThan(self, token, seconds):
        return (datetime.datetime.now() - token.time).total_seconds() > seconds

    def refreshTokens(self):
        for token in self.tokens:
            if self.isTokenOlderThan(token, 60):
                self.updateTokens()
                break

    def get_currentEthPrice(self):
        url = "https://api.etherscan.io/api?module=stats&action=ethprice"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        data = loads(response.text)

        return data['result']['ethusd']

    def get_currentBtcPrice(self):
        url = "https://api.binance.com/api/v3/ticker/price"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        data = loads(response.text)

        return data['price']

    def getEthAddressTokens(self, address):
        url = "https://api.etherscan.io/api?module=account&action=tokentx&address=" + address + "&startblock=0&endblock=999999999&sort=asc&apikey=YourApiKeyToken"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        data = loads(response.text)

        return data['result']

if __name__ == "__main__":
    cs = CryptoStats()
    print(cs.get_currentEthPrice())
    print(cs.get_currentBtcPrice())