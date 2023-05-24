from fyers_api import fyersModel
from fyers_api import accessToken
import requests
import datetime
import pandas as pd
import time
import pytz
from credentials import *

# Paste the access Token below
access_token = ""
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,log_path="logs/")
is_async = True

# USE THIS LIST IF YOU WANT TO FETCH DATA FOR MULTIPLE STOCKS IN ONE GO
stockList = pd.read_csv("nifty_200.csv")

# ASSIGN THE DATE RANGE FOR WHICH YOU WANT TO FETCH THE DATA
to_date = datetime.datetime.now().strftime("%Y-%m-%d")
from_date = datetime.date(2022,5,27).strftime("%Y-%m-%d")

# IF YOU WANT TO FETCH DATA FOR A SINGLE STOCK/INDEX, PLEASE REPLACE THE VALUE BELOW WITH THE SYMBOL OF THAT STOCK/INDEX.
symbol = "NSE:SBIN-EQ"
data = {"symbol":symbol,"resolution":"5","date_format":"1","range_from":from_date,"range_to":to_date,"cont_flag":"1"}
x = fyers.history(data)
# print(x)
df = pd.DataFrame.from_dict(x['candles'])
cols = ['datetime','open','high','low','close','volume']
df.columns = cols
# df.columns = cols
df['datetime'] = pd.to_datetime(df['datetime'],unit = "s")
df['datetime'] = df['datetime'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
df['datetime'] = df['datetime'].dt.tz_localize(None)
df = df.set_index('datetime')
# SAVE DATA TO CSV FILE
df.to_csv('Daily new/'+symbol+'.csv')

# IF YOU ARE FETCHING DATA FOR A SINGLE STOCK MAKE SURE YOU COMMENT OUT THE CODE BELOW BEFORE RUNNING THE SCRIPT

# CODE FOR FETCHING DATA FOR MULTIPLE STOCKS

def historical_bydate(symbol, sd, ed, interval=1):
    data = {"symbol": symbol, "resolution": "D", "date_format": "1", "range_from": str(sd), "range_to": str(ed),
            "cont_flag": "1"}
    nx = fyers.history(data)
    print(nx)
    cols = ['datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.DataFrame.from_dict(nx['candles'])
    df.columns = cols
    df['datetime'] = pd.to_datetime(df['datetime'], unit="s")
    df['datetime'] = df['datetime'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
    df['datetime'] = df['datetime'].dt.tz_localize(None)
    # df = df.set_index('datetime')
    return df

for stocks in stockList['Symbol']:
    start_date = datetime.date(2022, 6, 3)
    end_date = datetime.datetime.now().date()
    df = pd.DataFrame()

    # CALCULATING THE NUMBER OF DAYS BETWEEN FROM AND TO DATE
    n = abs((start_date - end_date).days)

    ab = None

    while ab == None:
        sd = (end_date - datetime.timedelta(days=n))
        ed = (sd + datetime.timedelta(days=99 if n > 100 else n)).strftime("%Y-%m-%d")
        sd = sd.strftime("%Y-%m-%d")
        dx = historical_bydate("NSE:"+stocks+"-EQ", sd, ed)
        df = df.append(dx)
        # IT IS IMPORTANT TO GET THE NUMBER OF DAYS BECASUE THE API ONLY ALLOWS TO FETCH DATA FOR 99 DAYS IN ONE GO
        n = n - 100 if n > 100 else n - n
        print(n)
        time.sleep(0.3)
        if n == 0:
            ab = "done"

    df['Date'] = df['datetime'].apply(lambda x: x.date().strftime('%Y-%m-%d'))
    df['Time'] = df['datetime'].apply(lambda x: x.time().strftime('%H:%M:%S'))
    df.to_csv('Daily new/'+stocks+'.csv')

