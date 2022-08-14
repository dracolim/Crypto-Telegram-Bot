import os
import datetime as date
from sqlite3 import paramstyle
import requests
from requests import Session
import telebot.secret as secret
from pprint import pp

# pprint => pp(r.json())


class CMC:
    # DOCUMENTATION: https://coinmarketcap.com/api/documentation
    # sends token
    def __init__(self, token):
        self.apiurl = 'https://pro-api.coinmarketcap.com'
        self.headers = headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': token,
        }
        self.session = Session()
        # go into session
        self.session.headers.update(self.headers)

    # get all coins
    def getAllCoins(self):
        url = self.apiurl + '/v1/cryptocurrency/map'
        r = self.session.get(url)
        data = r.json()['data']
        return data

    # get price by symbol
    def getPriceByTicker(self, symbol):
        symbol = symbol.upper()
        all_symbols = self.getAllSymbols()

        if symbol == '':
            return 'Enter a cryptocurrency ticker (/get_price_by_ticker BTC)'
        elif symbol not in all_symbols:
            return 'There is no such cryptocurrency 😔'
        else:
            url = self.apiurl + '/v1/cryptocurrency/quotes/latest'
            parameters = {
                'symbol': symbol
            }
            r = self.session.get(url, params=parameters)
            data = r.json()['data']
            price = data[symbol]['quote']['USD']['price']
            return str(round(price, 2)) + ' USD'

            #all_names = self.getAllNames()

    # get price by name
    def getPriceByName(self, name):
        all_name = self.getAllNames()
        all_coins = self.getAllCoins()

        if name == '':
            return 'Enter a cryptocurrency name (/get_price_by_ticker Bitcoin)'
        else:
            first_letter = name[0].upper()
            name2 = first_letter + name[1:].lower()
            if name2 not in all_name:
                return 'There is no such cryptocurrency'
            else:
                for each in all_coins:
                    if name2 == each['name']:
                        symbol = each['symbol']
                        price = self.getPriceByTicker(symbol)
            return price

    # get all the cryptocurrency symbols

    def getAllSymbols(self):
        full_data = self.getAllCoins()
        all_symbols = []
        for each in full_data:
            symbol = each['symbol']
            all_symbols.append(symbol)
        return all_symbols

    # get all the cryptocurrency names
    def getAllNames(self):
        full_data = self.getAllCoins()
        all_names = []
        for each in full_data:
            name = each['name']
            all_names.append(name)
        return all_names

    # TOP 10
    def getTopTen(self):
        data = self.getAllCoins()
        top_10 = {}
        top_10_string = ""

        for each in data:
            rank = each['rank']
            if rank <= 10:
                top_10[rank] = each['name'] + ' (' + each['symbol'] + ')'

        sorted_top_10 = dict(sorted(top_10.items()))

        for key in sorted_top_10:
            value = sorted_top_10[key]
            top_10_string += f"{str(key)}: {value} \n"

        return top_10_string


# creating cmc object
cmc = CMC(secret.API_KEY)

# pp(cmc.getPriceByID('bitCoin'))
