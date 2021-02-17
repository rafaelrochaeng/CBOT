import sqlite3 as sq
from datetime import datetime


class Database:
    def __init__(self):
        self.connection = None

    def create_db(self, day, currencies):
        self.connection = sq.connect("./Database/CBOT_DB_{}.sqlite".format(day))

        for currency in currencies:
            self.connection.execute('''CREATE TABLE IF NOT EXISTS {}_TICKS (
                                                          date           TEXT,
                                                          bid            REAL,
                                                          ask            REAL,
                                                          last           REAL);'''.format(currency.replace('/', '_')))

        return

    def insert_tick(self, tickers, symbols):

        for symbol in symbols:
            tick = tickers[symbol]['info']
            ask = tick['ask']
            last = tick['lastPrice']
            bid = tick['bid']
            timestamp = tick['timestamp']

            self.connection.execute('''INSERT INTO {}_TICKS (date,bid,ask,last)
                                    VALUES (?,?,?,?);'''.format(symbol.replace('/', '_')),
                                    (datetime.fromtimestamp(timestamp / 1000), bid, ask, last))

        self.connection.commit()

        return
