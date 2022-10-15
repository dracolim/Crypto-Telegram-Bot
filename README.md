# Crypto-Telegram-Bot
## Description
Crypto-Telegram-Bot allows you to get crypto updates such as news, price, supply , volume and percentage change. 
<br>
<br>
![example workflow](https://img.shields.io/badge/Build%20in-Python-blue)

## Tech Stack
Python, Heroku 

## Usage
1. Downlaod the <a href = 'https://telegram.org/'>Telegram</a> app
2. Search for the bot called <strong> know-your-crypto </strong> (@know_your_crypto_bot) or use the this <a href = 'https://t.me/know_your_crypto_bot'>Link</a>
3. Find the list of helper commands by entering ```/start```

## Commands
<img width="410" alt="Screenshot 2022-08-15 at 1 47 14 AM" src="https://user-images.githubusercontent.com/85498185/184548714-140f4c8d-d9b6-4933-8a66-6c7c12529cec.png">

<ins> ℹ️ Information </ins>
1. Get information about the cryptocurrency by symbol
```
/get_info_ticker <ticker>
```
<img width="306" alt="Screenshot 2022-08-15 at 1 51 49 AM" src="https://user-images.githubusercontent.com/85498185/184548874-52c60e7a-3d2e-480e-975d-07b31e8bed3a.png">

2. Get information about the cryptocurrency by name
```
/get_info_name <name>
```
<ins> 💲 Price </ins>
1. Get crypto price by symbol (in USD)
```
/get_price_by_ticker <ticker>
```
<img width="253" alt="Screenshot 2022-08-15 at 1 52 38 AM" src="https://user-images.githubusercontent.com/85498185/184548887-c0be9317-43db-4d13-813d-336034c64a51.png">

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
 <img width="360" alt="Screenshot 2022-08-15 at 1 51 16 AM" src="https://user-images.githubusercontent.com/85498185/184548859-818f59bc-bd10-451d-ac39-573f66294828.png">

<ins> 📰Updated News </ins>
1. Get all the latest news from different sources
```
/get_news
```
<img width="418" alt="Screenshot 2022-08-15 at 1 57 34 AM" src="https://user-images.githubusercontent.com/85498185/184549012-a3e8c09c-57c6-408f-aaba-6fe45aba9e11.png">

2. Get all the latest news from cointelegraph 
```
/get_news_cointelegraph
```
3. Get all the latest news about a cryptocurrency
```
/get_news_of <ticker>
```
## Deployment using Heroku
This telegram bot is deployed on heroku using the ```Procfile``` which is in the repository 

## APIs used
<ins> To get Price and trending cryptocurrencies </ins><br/>
| Description | Documentation |
| --- | --- |
| Coin Market Cap | https://coinmarketcap.com/api/documentation |

<br/>

<ins> To get exchange rate </ins> <br/>
| Description | Documentation |
| --- | --- |
| Fixer | https://apilayer.com/marketplace/fixer-api |


<br/>
<ins> To get news </ins> <br/>
| Description | Documentation |
| ------------- | ------------- |
| mboum-finance | https://rapidapi.com/sparior/api/mboum-finance/ |
| crypto-news-live3 | https://rapidapi.com/ddeshon/api/crypto-news-live3/ |
| crypto-news14 | https://rapidapi.com/enayfls-ibksP3yFoax/api/crypto-news14/ |

## What's next for this bot
1. Linking it to a database so that users can build their very own personal portfolio
2. Adding machine learning, creating OHLC graphs that can be send as an image through the telegram bot
