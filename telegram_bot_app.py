from datetime import date
from email import message
import os
from io import BytesIO
from urllib import request
from telegram.ext.messagehandler import MessageHandler

from telegram import ParseMode
from telegram import (
    Update,
    ReplyKeyboardMarkup
)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    ConversationHandler,
    Filters
)
import mplfinance as mpf
import _thread

# import all the functions from other .py files
from telebot.cmc_api import CMC
from telebot.coinbase import getOHLCgraph
from telebot.exchange_rate import getExchangeRate
from telebot.news import getNewsBySymbol, getTodayNews, getNewsFromCointelegraph
from telebot.secret import API_KEY, bot_token

print('Bot started...')

PORT = int(os.environ.get("PORT", 5000))
VERB = ["rose", "fell"]
COLOUR = ["🔴", "🟢"]
UPDATED = 0

TOKEN = bot_token

# date
today = date.today()
DATE = today.strftime("%b-%d-%Y")


def start(update: Update, context: CallbackContext) -> None:
    reply_text = 'Hi! I am your crypto bot 🤖. \n' + \
        f'How may I be of service today ({DATE})? \n'

    commands = "\n📝 Commands \n" + "/start - get commands \n"
    price = "\n💲 Price \n" + "/get_price_by_ticker TICKER: Get crypto price by symbol (in USD) \n" + "/get_price_by_name NAME: Get crypto price by name (in USD) \n" + \
        "/convert_exchange_rate PRICE CURRENCY: Convert price from USD to other currencies \n"
    top_10_command = f'\n💹 Trending \n /top_10_cryptocurrency: Top 10 cryptocurrency today \n'
    news = f'\n📰Updated News as of {DATE} \n/get_news: Get all the news from different sources \n' + \
        f"/get_news_cointelegraph: Get all the news from cointelegraph \n" + \
        f"/get_news_of CRYPTO: Get all the news about a cryptocurrency \n"

    reply_text += commands + price + top_10_command + news

    update.message.reply_text(reply_text)


# To get the price of the coin by SYMBOL
def get_price_by_ticker(
    update: Update,
    context: CallbackContext,
    symbol: str = None,
) -> None:

    symbol = update.message.text.split('/get_price_by_ticker')[1].strip()

    result = CMC(API_KEY).getPriceByTicker(symbol)
    # check if result is valid:
    if 'USD' not in result:
        message = result
    else:
        message = f"{symbol.upper()} changed by {result}!"

    update.message.reply_text(message)


# To get the price of the coin by NAME
def get_price_by_name(
    update: Update,
    context: CallbackContext,
    name: str = None,
) -> None:

    name = update.message.text.split('/get_price_by_name')[1].strip()

    result = CMC(API_KEY).getPriceByName(name)
    # check if result is valid:
    if 'USD' not in result:
        message = result
    else:
        first_letter = name[0].upper()
        name2 = first_letter + name[1:].lower()
        message = f"{name2} changed by {result}!"

    update.message.reply_text(message)


# To convert USD to other currency
def convert_exchange_rate(update: Update, context: CallbackContext, price: int = None, currency: str = None) -> None:
    message = ""
    # scenario 1: did not include price and currency
    if len(update.message.text.split()) == 1:
        message = 'Enter a price and currency and inlcude spacing (/convert_exchange_rate 128 SGD)'
    # scenario 2: only price, no currency
    elif len(update.message.text.split()) == 2 and update.message.text.split()[1].isdigit():
        message = 'Enter a currency (/convert_exchange_rate 128 SGD)'
    # scenario 3: no spacing
    elif len(update.message.text.split()) == 2 and any(char.isdigit() for char in update.message.text.split()[1]):
        message = 'Ensure there is a spacing between price and currency (/convert_exchange_rate 128 SGD)'
    # scenario 4: all is well
    elif len(update.message.text.split()) == 3:
        price = update.message.text.split()[1]
        currency = update.message.text.split()[2]

        new_price = getExchangeRate(price, currency)

        message = f"{price} USD = {new_price} SGD"
    # scenario 5: only currency, no price
    else:
        message = 'Enter a price (/convert_exchange_rate 128 SGD)'

    update.message.reply_text(message)


# To get top 10 coins
def get_top_ten(update: Update, context: CallbackContext) -> None:
    top_10 = CMC(API_KEY).getTopTen()
    message = f"Top 10 Cryptocurrency as of {DATE} ✨: \n{top_10}"

    update.message.reply_text(message)


# To get OHLC graph"
def send_photo(update: Update, context: CallbackContext) -> None:
    df_ohlc = getOHLCgraph()
    fig = mpf.plot(df_ohlc, type='candle', mav=(3, 6, 9), volume=True)

    plot_file = BytesIO()
    fig.savefig(plot_file, format='png')
    plot_file.seek(0)

    print(df_ohlc)

    update.message.reply_photo(plot_file)


# To get TODAY news
def get_today_news(update: Update, context: CallbackContext) -> None:
    news_list = getTodayNews()
    if len(news_list) == 0:
        message = f"📰 News as of {DATE}: \n\n" + '---No news today---'
    else:
        message = f"📰 News as of {DATE}: \n\n"
        for each_news in news_list:
            title = each_news['title']
            link = each_news['link']
            source = each_news['source']

            combine = f'⚫ Title: {title} \n🔗 LIink: {link} \nℹ️ Source: {source} \n\n'
            message += combine

    update.message.reply_text(message)


# To get news by symbol
def get_news_by_symbol(update: Update, context: CallbackContext, symbol: str = None,) -> None:
    if len(update.message.text.split()) == 1:
        message = 'Enter a crypto symbol (/get_news_of BTC)'
    else:
        symbol = update.message.text.split('/get_news_of')[1].strip()
        news_list = getNewsBySymbol(symbol)
        if len(news_list) == 0:
            message = f"📰 News as of {DATE}: \n\n" + '---No news today---'
        else:
            message = f"📰 News as of {DATE}: \n\n"
            for each_news in news_list:
                title = each_news['title']
                link = each_news['link']
                description = each_news['description']
                combine = f'⚫ Title: {title} \n📄 Description: {description} \n🔗 LIink: {link} \n\n'
                message += combine

    update.message.reply_text(message)


def get_news_cointelegraph(update: Update, context: CallbackContext) -> None:
    news_list = getNewsFromCointelegraph()
    if len(news_list) == 0:
        message = f"📰 News as of {DATE}: \n\n" + '---No news today---'
    else:
        message = f"📰 News as of {DATE}: \n\n"
        for each_news in news_list:
            title = each_news['title']
            description = each_news['desc']
            link = each_news['url']

            combine = f'⚫ Title: {title} \n📄 Description: {description} \n🔗 LIink: {link} \n\n'
            message += combine

    update.message.reply_text(message)


def main() -> None:
    updater = Updater(token=bot_token, use_context=True)

    # get dispatcher to register handlers
    dispatcher = updater.dispatcher

    # add handlers here
    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(CommandHandler(
        "get_price_by_ticker", get_price_by_ticker))
    dispatcher.add_handler(CommandHandler(
        "get_price_by_name", get_price_by_name))
    dispatcher.add_handler(CommandHandler(
        "convert_exchange_rate", convert_exchange_rate))

    dispatcher.add_handler(CommandHandler(
        "top_10_cryptocurrency", get_top_ten))
    dispatcher.add_handler(CommandHandler("OHLC_graph", send_photo))

    dispatcher.add_handler(CommandHandler("get_news", get_today_news))
    dispatcher.add_handler(CommandHandler("get_news_of", get_news_by_symbol))
    dispatcher.add_handler(CommandHandler(
        "get_news_cointelegraph", get_news_cointelegraph))

    # start the bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(
        'https://know-your-crypto-telegram-bot.herokuapp.com/' + TOKEN)
    #updater.start_polling()

    # block until the user proesses ctrl-c or the process receives SIGTINT,
    updater.idle()


if __name__ == '__main__':
    main()
