import os
from datetime import date, datetime
from sqlite3 import paramstyle
import requests
from pprint import pp

# date
today = datetime.now()
DATE = today.strftime("%Y-%m-%d")


def getNewsBySymbol(symbol):
    news_list = []
    url = "https://mboum-finance.p.rapidapi.com/ne/news/"
    querystring = {"symbol": symbol}

    headers = {
        "X-RapidAPI-Key": "608526d4bcmshba1018c85d9956bp13fedfjsn04bbfe9692f4",
        "X-RapidAPI-Host": "mboum-finance.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    if len(response.json()) == 2:
        return news_list
    else:
        data = response.json()['item']

        for each_news in data:
            news_list.append(each_news)

        return news_list[:5]


# pp(getNewsBySymbol('eth'))


def getTodayNews():
    news_list = []
    url = "https://mboum-finance.p.rapidapi.com/ne/news"

    headers = {
        "X-RapidAPI-Key": "608526d4bcmshba1018c85d9956bp13fedfjsn04bbfe9692f4",
        "X-RapidAPI-Host": "mboum-finance.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()

    for each_news in data:
        date = each_news['pubDate'][0:10]
        if date == DATE:
            news_list.append(each_news)

    return news_list[:5]


# pp(get_today_news())

def getNewsFromCointelegraph():
    news_list = []

    url = "https://crypto-news14.p.rapidapi.com/news/cointelegraph"
    headers = {
        "X-RapidAPI-Key": "608526d4bcmshba1018c85d9956bp13fedfjsn04bbfe9692f4",
        "X-RapidAPI-Host": "crypto-news14.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()

    for each_news in data:
        pubdate = each_news['date'][5:16]
        date = datetime.strptime(pubdate, "%d %b %Y").strftime('%Y-%m-%d')
        if date == '2022-08-22':
            news_list.append(each_news)

    return news_list[:5]

pp(getNewsFromCointelegraph())
