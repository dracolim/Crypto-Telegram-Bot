from io import BytesIO
import os
import datetime as date
from sqlite3 import paramstyle
from tokenize import PlainToken
import requests
from requests import Session
import telebot.secret as secret
from pprint import pp

from requests.exceptions import HTTPError
import pandas as pd
import json as js
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
# Uncomment this if you like to use the old MPL library

#from mpl_finance import candlestick_ohlc
import mplfinance as mpf
import matplotlib.dates as mpl_dates
import matplotlib.ticker as tkr
import seaborn as sns
from PIL import Image
import numpy as np
import math


# Set some standard parameters upfront
pd.options.display.float_format = '{:.1f}'.format
sns.set() # default seaborn look and feel
plt.style.use('ggplot')
REST_API = 'https://api.pro.coinbase.com'
PRODUCTS = REST_API+'/products'
# I am only interested in a few currencies that I want to trade, so let's add them here:
MY_CURRENCIES = ['BTC-EUR#','ETH-EUR','LTC-EUR','BCH-EUR'] 


#takes URL and param to return response library
def connect(url, *args, **kwargs):
    try:
        if kwargs.get('param', None) is not None:
            response = requests.get(url,params)
        else:
            response = requests.get(url)
        response.raise_for_status()
        #print('HTTP connection success!')
        return response
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

#1. connect to REST Endpoint
response = connect(PRODUCTS)
response_content = response.content
response_text = response.text
response_headers = response.headers

#2. get currency information
df_currencies = pd.read_json (response_text)
#print("\nNumber of columns in the dataframe: %i" % (df_currencies.shape[1]))
#print("Number of rows in the dataframe: %i\n" % (df_currencies.shape[0]))
columns = list(df_currencies.columns)
#print(columns)
#print() 
df_currencies[df_currencies.id.isin(MY_CURRENCIES)][['id', 'base_currency', 'quote_currency', 'quote_increment', 'base_increment']].head(5)

#3. Currency statistics 
currency_rows = []
for currency in MY_CURRENCIES:
    response = connect(PRODUCTS+'/'+currency+'/stats')
    response_content = response.content
    data = js.loads(response_content.decode('utf-8'))
    currency_rows.append(data)
# Create dataframe and set row index as currency name
df_statistics = pd.DataFrame(currency_rows, index = MY_CURRENCIES)
#print(df_statistics)

#4. Bitcoin historic data (over last 90 days etc.)
start_date = (datetime.today() - timedelta(days=90)).isoformat()
end_date = datetime.now().isoformat()
# Please refer to the coinbase documentation on the expected parameters
params = {'start':start_date, 'end':end_date, 'granularity':'86400'}
response = connect(PRODUCTS+'/ETH-USD/candles', param = params)
response_text = response.text
df_history = pd.read_json(response_text)
# Add column names in line with the Coinbase Pro documentation
df_history.columns = ['time','low','high','open','close','volume']

# We will add a few more columns just for better readability
df_history['date'] = pd.to_datetime(df_history['time'], unit='s')
df_history['year'] = pd.DatetimeIndex(df_history['date']).year
df_history['month'] = pd.DatetimeIndex(df_history['date']).month
df_history['day'] = pd.DatetimeIndex(df_history['date']).day
# Only display the first 5 rows
df_history.head(5).drop(['time','date'], axis=1)

#print(df_history)

#5. OHLC chart
# Make a copy of the original dataframe
df_ohlc = df_history
# Remove unnecessary columns and only show the last 30 days
df_ohlc = df_ohlc.drop(['time','year','month','day'], axis = 1).head(30)
# Columns must be in a specific order for the candlestick chart (OHLC)
df_ohlc = df_ohlc[['date', 'open', 'high', 'low', 'close','volume']]
# Index must be set as the date
df_ohlc.set_index('date', inplace=True)
# Inverse order is expected so let's reverse the rows in the dataframe
df_ohlc = df_ohlc[::-1]

#mpf.plot(df_ohlc,type='candle',mav=(3,6,9),volume=True)

image_buf = BytesIO()
plt.savefig(image_buf, format = 'png')
plt.show()


im = Image.open(image_buf)
im.show(title = 'my imafe')

image_buf.close

