import ccxt
import json
from datetime import datetime, date, timedelta
import sqlite3 as sq
import time
from Database import Database
from Exchange import Exchange

with open('account_settings.json') as file:
    settings = json.load(file)
    api_key = settings["api_key"]
    secret_key = settings["secret_key"]

with open('app_settings.json') as file:
    settings = json.load(file)
    delay_update_minutes = settings["delay_update_minutes"]
    delay_data_acquisition = settings["delay_data_acquisition"]

symbols = ['BTC/BRL', 'ETH/BRL', 'BCH/BRL', 'XRP/BRL', 'BSV/BRL', 'DOT/BRL', 'DAI/BRL', 'NPXS/BRL',
           'DGB/BRL', 'DCR/BRL', 'XMR/BRL', 'XLM/BRL', 'WAVES/BRL', 'ETC/BRL', 'TRX/BRL', 'BTT/BRL',
           'EOS/BRL', 'ADA/BRL', 'BNB/BRL', 'LINK/BRL', 'DASH/BRL', 'LTC/BRL', 'XTZ/BRL', 'IOTA/BRL',
           'OMG/BRL', 'DOGE/BRL', 'NULS/BRL', 'BRZ/BRL',

           'BTC/EUR', 'ETH/EUR', 'BCH/EUR', 'XRP/EUR', 'DGB/EUR', 'BSV/EUR', 'DAI/EUR', 'EOS/EUR',
           'LTC/EUR', 'NULS/EUR', 'BTC/USDT', 'ETH/USDT', 'BCH/USDT', 'XRP/USDT', 'BSV/USDT', 'DOT/USDT',
           'DAI/USDT', 'NPXS/USDT', 'DGB/USDT', 'WAVES/USDT', 'XTZ/USDT', 'XLM/USDT', 'ETC/USDT', 'DCR/USDT',
           'OMG/USDT', 'TRX/USDT', 'BTT/USDT', 'EOS/USDT', 'ADA/USDT', 'BNB/USDT','LINK/USDT', 'DASH/USDT',
           'LTC/USDT', 'IOTA/USDT', 'DOGE/USDT', 'NULS/USDT', 'BRZ/USDT', 'XMR/USDT',

           'ETH/BTC', 'BCH/BTC', 'XRP/BTC', 'WAVES/BTC', 'XTZ/BTC', 'XLM/BTC', 'TRX/BTC', 'BTT/BTC',
           'EOS/BTC', 'ADA/BTC', 'BNB/BTC', 'LINK/BTC', 'DASH/BTC', 'LTC/BTC', 'IOTA/BTC', 'DOGE/BTC',
           'NULS/BTC', 'BRZ/BTC',

           'WAVES/ETH', 'XLM/ETH', 'XTZ/ETH', 'BTT/ETH', 'EOS/ETH', 'LINK/ETH', 'ADA/ETH', 'IOTA/ETH',
           'NULS/ETH', 'BRZ/ETH'
           ]

# Instances
database = Database()
exchange = Exchange(exchange='novadax', api_key=api_key, secret_key=secret_key)

today = None
start_update = datetime.now()+timedelta(minutes=delay_update_minutes)
conn = None

while True:
    if date.today() is not today:
        today = date.today()
        database.create_db(str(date.today()).replace('-', '_'), symbols)

    if datetime.now() >= start_update:
        start_update = datetime.now()+timedelta(minutes=delay_update_minutes)
        exec(open("UpdateCode.py").read())
        quit()

    tickers = exchange.get_tick()

    database.insert_tick(tickers, symbols)

    time.sleep(delay_data_acquisition)
