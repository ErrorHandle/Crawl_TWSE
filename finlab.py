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
#-------------------------------------------------------------------------------
# def crawl_price(date):
#     r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + str(date).split(' ')[0].replace('-','') + '&type=ALL')
#     ret = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '})
#                                         for i in r.text.split('\n')
#                                         if len(i.split('",')) == 17 and i[0] != '='])), header=0)
#     ret = ret.set_index('證券代號')
#     ret['成交金額'] = ret['成交金額'].str.replace(',','')
#     ret['成交股數'] = ret['成交股數'].str.replace(',','')
#     return ret
#
#
# data = {}
# n_days = 500
# date = datetime.datetime.now()
# fail_count = 0
# allow_continuous_fail_count = 100
# while len(data) < n_days:
#
#     print('parsing', date)
#     # 使用 crawPrice 爬資料
#     try:
#         # 抓資料
#         data[date.date()] = crawl_price(date)
#         print('success!')
#         fail_count = 0
#     except:
#         # 假日爬不到
#         print('fail! check the date is holiday')
#         fail_count += 1
#         if fail_count == allow_continuous_fail_count:
#             raise
#             break
#
#     # 減一天
#     date -= datetime.timedelta(days=1)
#     time.sleep(6)
#
# # data = pd.DataFrame({k:d for k, d in data.items()})
#
#
# open = pd.DataFrame({k:d['開盤價'] for k,d in data.items()}).transpose()
# open.index = pd.to_datetime(open.index)
# open.to_csv('10_open.csv')
#
# high = pd.DataFrame({k:d['最高價'] for k,d in data.items()}).transpose()
# high.index = pd.to_datetime(high.index)
# high.to_csv('10_high.csv')
#
# low = pd.DataFrame({k:d['最低價'] for k,d in data.items()}).transpose()
# low.index = pd.to_datetime(low.index)
# low.to_csv('10_low.csv')
#
# volume = pd.DataFrame({k:d['成交股數'] for k,d in data.items()}).transpose()
# volume.index = pd.to_datetime(volume.index)
# volume.to_csv('10_volume.csv')
#
# close = pd.DataFrame({k:d['收盤價'] for k,d in data.items()}).transpose()
# close.index = pd.to_datetime(close.index)
# close.to_csv('10_close.csv')

#-------------------------------------------------------------------------------

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


tsmc = {
    'close':close['2409'].dropna().astype(float),
    'open':open['2409'].dropna().astype(float),
    'high':high['2409'].dropna().astype(float),
    'low':low['2409'].dropna().astype(float),
    'volume': volume['2409'].dropna().astype(float),
}



df = pd.DataFrame(tsmc, index=tsmc['close'].index)
df.index.name = 'Date'
df.rename(columns={'open':'Open', 'close':'Close', 'low': 'Low', 'high':'High', 'volume':'Volume'}, inplace=True)
# index 與 data都做 reverse
df = df.sort_index(ascending=True)
#10MA / volume / close price
mpf.plot(df[300:],type='line',volume=True, mav=(5,20,60))

MACD = pd.DataFrame(abstract.MACD(tsmc)).transpose()
MACD.index = tsmc['close'].index
MACD.plot(grid=True, title='MACD')
plt.show()

RSI = pd.DataFrame(abstract.RSI(tsmc))
RSI.index = tsmc['close'].index
RSI.plot(grid=True, title='RSI')
plt.show()

KD = pd.DataFrame(abstract.STOCH(tsmc)).transpose()
KD.index = tsmc['close'].index
KD.plot(grid=True, title='KD')
plt.show()

# fig = plt.figure(figsize=(24, 8))
# ax = fig.add_subplot(1, 1, 1)
# #設定座標數量及所呈現文字
# ax.set_xticks(range(0, len(tsmc['close'].index), 10))
# ax.set_xticklabels(tsmc['close'].index[::10],rotation=90)
# #使用mpl_finance套件candlestick2_ochl
# mpf.plot(tsmc,type='candle',mav=(3,6,9),volume=True)
# MACD.plot()
# plt.show()

# ax = plt.gca()
# ax.

# tsmc['close'].plot()
# plt.show()
# tsmc['volume']['2020'].plt.bar()
# plt.show()
# print(open)
# open.index = pd.to_datetime(open[np.nan])
# open.drop([np.nan], axis=1, inplace=True)
# open[1101.0].plot()
# plt.show()




# print(open.index)
# b = open.fillna('date')
# print(open)
# print(b)
# print(open.head(10))
# open.index = pd.to_datetime(open[0])
# print(open.head(10))
# a = open.drop([0], axis=1)
# a['2330'].plot()
# plt.show()
# print(a.index[0])
# print(a)
# a.set_cl
# print(a)
#     print(k)
#     print(v)
# # tsmc = {
#     'close':close['2330']['2019'].dropna().astype(float),
#     'open':open['2330']['2019'].dropna().astype(float),
#     'high':high['2330']['2019'].dropna().astype(float),
#     'low':low['2330']['2019'].dropna().astype(float),
#     'volume': volume['2019']['2017'].dropna().astype(float),
# }
# tsmc['close'].plot()
# plt.show()
# # close.index = pd.to_datetime(close.index)
# close['2884'].plot()
# plt.show()
# close.index = pd.to_datetime(close.index)
# close['2330']['2020'].plot()
# # print(close['2330'])
# plt.show()

# def monthly_report(year, month):
#
#     # 假如是西元，轉成民國
#     if year > 1990:
#         year -= 1911
#
#     url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'_0.html'
#     if year <= 98:
#         url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'.html'
#
#     # 偽瀏覽器
#     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#
#     # 下載該年月的網站，並用pandas轉換成 dataframe
#     r = requests.get(url, headers=headers)
#     r.encoding = 'big5'
#
#     dfs = pd.read_html(StringIO(r.text), encoding='big-5')
#
#     df = pd.concat([df for df in dfs if df.shape[1] <= 11 and df.shape[1] > 5])
#
#     if 'levels' in dir(df.columns):
#         df.columns = df.columns.get_level_values(1)
#     else:
#         df = df[list(range(0,10))]
#         column_index = df.index[(df[0] == '公司代號')][0]
#         df.columns = df.iloc[column_index]
#
#     df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')
#     df = df[~df['當月營收'].isnull()]
#     df = df[df['公司代號'] != '合計']
#
#     # 偽停頓
#     time.sleep(5)
#
#     return df
