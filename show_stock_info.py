import requests
from io import StringIO
import pandas as pd
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from talib import abstract
import talib
import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc

open = pd.read_csv('./10_open.csv', header=None)
open = pd.DataFrame({v[0]:v[1:] for k, v in open.items()})
# open.index = open.loc[:, np.nan]
# print(open)
##### 透過 iloc
open.index = pd.to_datetime(open.iloc[::,0])
open.drop([np.nan], axis=1, inplace=True)
open.columns = open.columns.astype(str)
for i in range(len(open.columns.values)):
    open.columns.values[i] = open.columns.values[i].replace('.0', '')


close = pd.read_csv('./10_close.csv', header=None)
close = pd.DataFrame({v[0]:v[1:] for k, v in close.items()})
close.index = pd.to_datetime(close.iloc[::,0])
close.drop([np.nan], axis=1, inplace=True)
close.columns = close.columns.astype(str)
for i in range(len(close.columns.values)):
    close.columns.values[i] = close.columns.values[i].replace('.0', '')

high = pd.read_csv('./10_high.csv', header=None)
high = pd.DataFrame({v[0]:v[1:] for k, v in high.items()})
high.index = pd.to_datetime(high.iloc[::,0])
high.drop([np.nan], axis=1, inplace=True)
high.columns = high.columns.astype(str)
for i in range(len(high.columns.values)):
    high.columns.values[i] = high.columns.values[i].replace('.0', '')

low = pd.read_csv('./10_low.csv', header=None)
low = pd.DataFrame({v[0]:v[1:] for k, v in low.items()})
low.index = pd.to_datetime(low.iloc[::,0])
low.drop([np.nan], axis=1, inplace=True)
low.columns = low.columns.astype(str)
for i in range(len(low.columns.values)):
    low.columns.values[i] = low.columns.values[i].replace('.0', '')

volume = pd.read_csv('./10_volume.csv', header=None)
volume = pd.DataFrame({v[0]:v[1:] for k, v in volume.items()})
volume.index = pd.to_datetime(volume.iloc[::,0])
volume.drop([np.nan], axis=1, inplace=True)
volume.columns = volume.columns.astype(str)

for i in range(len(volume.columns.values)):
    volume.columns.values[i] = volume.columns.values[i].replace('.0', '')

stock = {
    'close':close['2409'].dropna().astype(float),
    'open':open['2409'].dropna().astype(float),
    'high':high['2409'].dropna().astype(float),
    'low':low['2409'].dropna().astype(float),
    'volume': volume['2409'].dropna().astype(float),
}



df = pd.DataFrame(stock, index=stock['close'].index)
df.index.name = 'Date'
df.rename(columns={'open':'Open', 'close':'Close', 'low': 'Low', 'high':'High', 'volume':'Volume'}, inplace=True)
# index 與 data都做 reverse
df = df.sort_index(ascending=True)
#10MA / volume / close price
mpf.plot(df[300:],type='line',volume=True, mav=(5,20,60))

MACD = pd.DataFrame(abstract.MACD(stock)).transpose()
MACD.index = stock['close'].index
MACD.plot(grid=True, title='MACD')
plt.show()

RSI = pd.DataFrame(abstract.RSI(stock))
RSI.index = stock['close'].index
RSI.plot(grid=True, title='RSI')
plt.show()

KD = pd.DataFrame(abstract.STOCH(stock)).transpose()
KD.index = stock['close'].index
KD.plot(grid=True, title='KD')
plt.show()



