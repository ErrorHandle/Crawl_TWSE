import requests
import datetime
import pandas as pd
from io import StringIO
import time
import numpy as np
import  matplotlib.pyplot  as  plt
from talib import abstract

def crawl_price(date):
    r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + str(date).split(' ')[0].replace('-','') + '&type=ALL')
    ret = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '})
                                        for i in r.text.split('\n')
                                        if len(i.split('",')) == 17 and i[0] != '='])), header=0)

    ret = ret.set_index('證券代號')
    ret['成交金額'] = ret['成交金額'].str.replace(',','')
    ret['成交股數'] = ret['成交股數'].str.replace(',','')
    return ret



def monthly_report(year, month):
    #西元轉民國
    if year > 1990:
        year -= 1911
    url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_' + str(year) + '_' + str(month) + '_0.html'
    if year <= 98:
        url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    }

    print(url)
    r = requests.get(url, headers=headers)
    r.encoding = 'big5'
    dfs = pd.read_html(StringIO(r.text), encoding='big-5')
    df = pd.concat([df for df in dfs if df.shape[1] <= 11 and df.shape[1] > 5])
    if 'levels' in dir(df.columns):
        df.columns = df.columns.get_level_values(1)
    else:
        df = df[list(range(0,10))]
        column_index = df.index[(df[0] == '公司代號')][0]
        df.columns = df.iloc[column_index]

    df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')
    df = df[~df['當月營收'].isnull()]
    df = df[df['公司代號'] != '合計']
    # 偽停頓
    time.sleep(5)
    return df

def set_time():
    weekday = datetime.now().isoweekday()
    nowday = datetime.now().strftime('%d')
    if weekday == 6:
        day = int(nowday) - 1
        current_day = str(day)

    elif weekday == 7:
        day = int(nowday) - 2
        current_day = str(day)
    else:
        current_day = datetime.now().strftime('%d')

    return datetime.now().strftime('%Y%m') + current_day


def pe_ratio(df, value):
# df.to_excel('123.xls')
    result = df[pd.to_numeric(df['本益比'], errors='coerce') > value].head(10)
    return result
# s.to_excel('本益比20.xls')
# print(s)


# 顯示出來
def crawl_serialday():
    data = {}
    n_days = 300
    date = datetime.datetime.now()
    fail_count = 0
    allow_continuous_fail_count = 30
    while len(data) < n_days:

        print('parsing', date)
        # 使用 crawPrice 爬資料
        try:
            # 抓資料
            data[date.date()] = crawl_price(date)
            print('success!')
            fail_count = 0
        except:
            # 假日爬不到
            print('fail! check the date is holiday')
            fail_count += 1
            if fail_count == allow_continuous_fail_count:
                raise
                break

        # 減一天
        date -= datetime.timedelta(days=1)
        time.sleep(7)
    close = pd.DataFrame({k:d['收盤價'] for k,d in data.items()}).transpose()
    close.index = pd.to_datetime(close.index)
    open = pd.DataFrame({k:d['開盤價'] for k,d in data.items()}).transpose()
    open.index = pd.to_datetime(open.index)

    high = pd.DataFrame({k:d['最高價'] for k,d in data.items()}).transpose()
    high.index = pd.to_datetime(high.index)

    low = pd.DataFrame({k:d['最低價'] for k,d in data.items()}).transpose()
    low.index = pd.to_datetime(low.index)

    volume = pd.DataFrame({k:d['成交股數'] for k,d in data.items()}).transpose()
    volume.index = pd.to_datetime(volume.index)

    tsmc = {
        'close':close['2330']['2020'].dropna().astype(float),
        'open':open['2330']['2020'].dropna().astype(float),
        'high':high['2330']['2020'].dropna().astype(float),
        'low':low['2330']['2020'].dropna().astype(float),
        'volume': volume['2330']['2020'].dropna().astype(float),
    }
    tsmc['close'].plot()
    plt.show()


    ret = talib2df(abstract.MACD(tsmc))
    ret.index = tsmc['close'].index
    ret.plot()
    tsmc['close'].plot(secondary_y=True).plot()
    plt.show()

    ret = talib2df(abstract.STOCH(tsmc))
    ret.index = tsmc['close'].index
    ret.plot()
    tsmc['close'].plot(secondary_y=True).plot()
    plt.show()




def talib2df(talib_output):
    if type(talib_output) == list:
        ret = pd.DataFrame(talib_output).transpose()
    else:
        ret = pd.Series(talib_output)
    return ret;

def main():
    # current_time = set_time()
    # url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + current_time + "&type=ALL"
    # r = requests.post(url)
    # #整理表格
    # df = pd.read_csv(StringIO(r.text.replace("=", "")), header=["證券代號" in l for l in r.text.split("\n")].index(True)-1)
    # df = df.apply(lambda s: pd.to_numeric(s.replace(",", "").replace("+", "1").replace("-", "-1"), errors='ignore'))
    tsmc = crawl_serialday()

main()
