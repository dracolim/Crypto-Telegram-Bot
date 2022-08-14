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


# Set some standard parameters upfront
pd.options.display.float_format = '{:.1f}'.format
sns.set() # default seaborn look and feel
plt.style.use('ggplot')
REST_API = 'https://api.pro.coinbase.com'
PRODUCTS = REST_API+'/products'
# I am only interested in a few currencies that I want to trade, so let's add them here:
MY_CURRENCIES = ['BTC-EUR#','ETH-EUR','LTC-EUR','BCH-EUR'] 


#takes URL and param to return response library
def connect(url, param):
    try:
        if param is not None:
            response = requests.get(url,param)
        else:
            response = requests.get(url)
        response.raise_for_status()
        #print('HTTP connection success!')
        return response
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

def getOHLCgraph():
    # GET HISTORIC DATA (over last 90 days etc.)
    start_date = (datetime.today() - timedelta(days=90)).isoformat()
    end_date = datetime.now().isoformat()
        # Refer to the coinbase documentation on the expected parameters
    params = {'start':start_date, 'end':end_date, 'granularity':'86400'}
    print(params)
    response = connect(PRODUCTS+'/BTC-USD/candles', param = params)
    response_text = response.text
    df_history = pd.read_json(response_text)
        # Add column names in line with the Coinbase Pro documentation
    df_history.columns = ['time','low','high','open','close','volume']

        # Add a few more columns just for better readability
    df_history['date'] = pd.to_datetime(df_history['time'], unit='s')
    df_history['year'] = pd.DatetimeIndex(df_history['date']).year
    df_history['month'] = pd.DatetimeIndex(df_history['date']).month
    df_history['day'] = pd.DatetimeIndex(df_history['date']).day

    #OHLC CHART
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
    #image = BytesIO()
    #plt.savefig

    

    return df_ohlc

    #plot_file = BytesIO()
    # fig.savefig(plot_file , format = 'png')
    # plot_file.seek(0)

    # return plot_file

getOHLCgraph()


# class ProcessPlotter:
#     def __init__(self):
#         self.x = []
#         self.y = []

#     def terminate(self):
#         plt.close('all')

#     def call_back(self):
#         while self.pipe.poll():
#             command = self.pipe.recv()
#             if command is None:
#                 self.terminate()
#                 return False
#             else:
#                 self.x.append(command[0])
#                 self.y.append(command[1])
#                 self.ax.plot(self.x, self.y, 'ro')
#         self.fig.canvas.draw()
#         return True

#     def __call__(self, pipe):
#         print('starting plotter...')

#         self.pipe = pipe
#         self.fig, self.ax = plt.subplots()
#         timer = self.fig.canvas.new_timer(interval=1000)
#         timer.add_callback(self.call_back)
#         timer.start()

#         print('...done')
#         plt.show()

# class NBPlot:
#     def __init__(self):
#         self.plot_pipe, plotter_pipe = mp.Pipe()
#         self.plotter = ProcessPlotter()
#         self.plot_process = mp.Process(
#             target=self.plotter, args=(plotter_pipe,), daemon=True)
#         self.plot_process.start()

#     def plot(self, finished=False):
#         send = self.plot_pipe.send
#         if finished:
#             send(None)
#         else:
#             data = np.random.random(2)
#             send(data)


# def main():
#     pl = NBPlot()
#     for ii in range(10):
#         pl.plot()
#         time.sleep(0.5)
#     pl.plot(finished=True)


# if __name__ == '__main__':
#     if plt.get_backend() == "MacOSX":
#         mp.set_start_method("forkserver")
#     main()



