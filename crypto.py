# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 19:16:22 2018

@author: utkuarik
"""
# import dateparser
import pytz
import time
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
# from binance.client import Client
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt



def rsif_calc(df, period, data):

    prof = 0
    defic = 0

    for i in range (period - 1):

        if ( i > 0 ) & (data[i] > data[i - 1]):
             prof = prof + data[i] - data[i - 1]

        elif  (i>0) & (data[i] < data[i - 1]):
             defic = defic +  data[i - 1] - data[i]

    prof = prof/period
    defic = defic/period

    df.at[13,"prof"] = prof
    df.at[13,"defic"] = defic
    df.at[13, "RSI"] = 100*prof / (prof+defic)

    return df, data


def rsi_calc(df, period, data):

    for i in range (0, len(data) - period ):

        prof = 0
        defic = 0

        prof = (13 * df.at[period - 1 + i, "prof"] + (data[i + period] > data[period +i - 1])*
        (data[i + period] - data[period +i - 1]))/14

        defic = (13 * df.at[period - 1 + i, "defic"] + (data[i + period] < data[period +i - 1])*
        (data[i + period - 1] - data[period +i ]))/14

        df.at[i + period, "prof"] = prof
        df.at[i + period, "defic"] = defic
        df.at[i + period, "RSI"] = 100 - 100 / (1 + prof/defic)
    return df, data


def find_trade(invest, coin_list, period):

    for coin in coin_list:

        try:
            klines = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1DAY, "60 day ago UTC")
        except Exception:
            pass

        klines = np.array(klines)

        if len(klines) < 60:
            continue
        df = pd.DataFrame()
        df = pd.DataFrame(data=klines, columns=["Open time", "Open", "High", "Low", "Close", "Volume",
        "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume"
        , "Taker buy quote asset volume", "Ignore"])
        print(coin)
        data = np.array(df["Close"])
        data = data.astype(np.float)


        # print(df)
        df, data = rsif_calc(df, 14,data)
        # print(df)
        df, data = rsi_calc(df, 14, data)
        # print(df)
        df, data = stoch_rsi(df, 14, data)
        # print(df)

        if df.at[len(data)-1, "RSI"] < 30:
         invest['RSI'].append(coin)

        if df.at[len(data)-1, "StochRSI"] < 15:
         invest['StochRSI'].append(coin)

    return invest


def mov_ave(invest, ma_period):
    for coin in coin_list:

         ma = 0.0
         klines = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1DAY,
                                               "60 day ago UTC",
                                               )


         klines = np.array(klines)

         df = pd.DataFrame(data=klines, columns=["Open time", "Open", "High", "Low", "Close", "Volume",
        "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume"
        , "Taker buy quote asset volume", "Ignore"])

         data = np.array(df["Close"])

         data = data.astype(np.float)

         if(len(data)<60):
             continue

         for i in range (10):

             ma = ma + float(df.at[i + len(data) - 10, "Close"])
         ma = ma / 10

         if float(df.at[len(data) - 1, "Close"]) > ma:

             invest['MA'].append(coin)

    return print(invest)


def stoch_rsi(df, period, data):

    for i in range (0, len(data) - period+1 ):

        low = df.at[i, "RSI"]
        high = df.at[i, "RSI"]
        for j in range(period):

            if(low > df.at[i+j,"RSI"]):
                low = df.at[i+j, "RSI"]
            if(high < df.at[i+j, "RSI"]):
                high = df.at[i+j, "RSI"]

        df.at[i + period-1, "StochRSI"] = (df.at[i + period-1, "RSI"] - low)/ (high - low)*100
    return df, data

def plot_coin(coin_list):


 for coin in coin_list:
    try:
        klines = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1DAY, "60 day ago UTC")
    except Exception:
        continue

    klines_data = pd.DataFrame(np.array(klines))

    x = klines_data.index.values[::-1]
    y = klines_data[4].apply(lambda x: float(x))

    # creating the canvas 
    fig = plt.figure() 
    
    # setting size of first canvas 
    axes1 = fig.add_axes([0, 0, 0.7, 1]) 

    # remove right and top border
    axes1.spines['top'].set_visible(False)
    axes1.spines['right'].set_visible(False)

    # name the labels
    axes1.set_xlabel('Index', fontsize=20)
    axes1.set_ylabel('Value',fontsize=20)
    
    # plotting graph of first canvas 
    axes1.plot(x, y) 
   
    axes1.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    axes1.legend(bbox_to_anchor=(1, 1), loc='best', borderaxespad=0. , prop={'size':10})
    # displaying both graphs 
    plt.show()
if __name__ == "__main__":

# Enter your api key and secret key here
    client = Client("","")
    coin_list = ["ETHBTC","TRXBTC","IOSTBTC","ICXBTC","VENBTC","WTCBTC","XLMBTC","ELFBTC","CNDBTC","TNTBTC","XRPBTC",
    "NEOBTC","BNBBTC","ADABTC","EOSBTC","TNBBTC","HSRBTC","LTCBTC","XVGBTC","RCNBTC","POEBTC","CDTBTC","NEBLBTC",
    "IOTABTC","PIVXBTC","BCCBTC","BCDBTC","BATBTC","LENDBTC","VIBEBTC","MANABTC","OMGBTC","BRDBTC","MTLBTC","BTSBTC","RLCBTC","ENJBTC",
    "GTOBTC","QTUMBTC","ETCBTC","SNGLSBTC","APPCBTC","AIONBTC","AMBBTC","SUBBTC","XMRBTC","FUNBTC","ZRXBTC","LSKBTC","SNTBTC","OAXBTC","INSBTC",
    "PPTBTC","QSPBTC","ENGBTC","WINGSBTC","MDABTC","LRCBTC","GASBTC","BTGBTC","CTRBTC","STRATBTC","ARKBTC",
    "POWRBTC","LINKBTC","WAVESBTC","TRIGBTC","WABIBTC","KNCBTC","DASHBTC","OSTBTC","REQBTC","SALTBTC","FUELBTC",
    "KMDBTC","STORJBTC","ARNBTC","ZECBTC","MCOBTC","DLTBTC","LUNBTC","CMTBTC","EDOBTC","BQXBTC","ASTBTC",
    "BCPTBTC","EVXBTC","RDNBTC","VIBBTC","MODBTC","GXSBTC","DNTBTC","NULSBTC","XZCBTC","NAVBTC","ADXBTC",
    "YOYOBTC","DGDBTC","SNMBTC","GVTBTC","MTHBTC",
    "ICNBTC","BNTBTC","DATABTC"

    ]

    # coin_list = ["ETHBTC","TRXBTC", "MANABTC"]
    
    data = 0
    invest = {'RSI':[], 'MA':[], 'StochRSI':[]}
    
    invest = find_trade(invest,coin_list, 14)
    print(invest['StochRSI'])
    # plot_coin(invest['StochRSI'])

    #plt.plot(df["Close"])
    #plt.show()