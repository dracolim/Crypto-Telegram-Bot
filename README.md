# Crypto-Telegram-Bot
## Description
Crypto-Telegram-Bot allows you to get crypto updates such as news, price, supply , volume and percentage change. 

## Tech Stack
Python, Heroku 

## Usage
1. Downlaod the <a href = 'https://telegram.org/'>Telegram</a> app
2. Search for the bot called <strong> know-your-crypto </strong> (@know_your_crypto_bot) or use the this <a href = 'https://t.me/know_your_crypto_bot'>Link</a>
3. Find the list of helper commands by entering ```/start```

## Commands
<ins> ℹ️ Information </ins>
1. Get information about the cryptocurrency by symbol
```
/get_info_ticker <ticker>
```
2. Get information about the cryptocurrency by name
```
/get_info_name <name>
```
<ins> 💲 Price </ins>
1. Get crypto price by symbol (in USD)
```
/get_price_by_ticker <ticker>
```
2. Get crypto price by name (in USD)
```
/get_price_by_name <name>
```
3. Convert amount from USD to other currencies
```
/convert_exchange_rate <price> <currency code>
```
<ins> 💹 Trending </ins>
1. Get top 10 cryptocurrncy as of today
```
 /top_10_cryptocurrency
 ```
<ins> 📰Updated News </ins>
1. Get all the latest news from different sources
```
/get_news
```
2. Get all the latest news from cointelegraph 
```
/get_news_cointelegraph
```
3. Get all the latest news about a cryptocurrency
```
/get_news_of <cryptocurrency>
```
## Deployment using Heroku
This telegram bot is deployed on heroku using the ```Procfile``` which is in the repository 

## APIs used
<ins> To get Price and trending cryptocurrencies </ins><br/>
1.Coin Market Cap - https://coinmarketcap.com/api/documentation
<br/>
<ins> To get exchange rate </ins> <br/>
2. Fixer - https://apilayer.com/marketplace/fixer-api
<br/>
<ins> To get news </ins> <br/>
3. mboum-finance - https://rapidapi.com/sparior/api/mboum-finance/ <br/>
4. crypto-news-live3 - https://rapidapi.com/ddeshon/api/crypto-news-live3/ <br/>
5. crypto-news14 - https://rapidapi.com/enayfls-ibksP3yFoax/api/crypto-news14/ <br/>

## What's next for this bot
1. Linking it to a database so that users can build their very own personal portfolio
2. Adding machine learning, creating OHLC graphs that can be send as an image through the telegram bot
