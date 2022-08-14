import os
from sqlite3 import paramstyle
import requests
from pprint import pp

def getExchangeRate(price, currency):
    url = f"https://api.apilayer.com/fixer/convert?to={currency}&from=USD&amount={price}"
    payload = {}
    headers= {
    "apikey": "JkEvvoMtQojPlvPKoJ6wahFdLv9GeeRk"
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    data = response.json()

    new_price = data['result']

    return str(round(new_price,2))


#pp(get_exchange_rate(2, 'SGD'))