from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, \
    Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
import requests
import re
import psycopg2
import cjson
from bs4 import BeautifulSoup


engine = create_engine('postgresql+psycopg2://localhost/stock_analysis')
Base = declarative_base()


class Stock(Base):
    __tablename__ = 'symbols'
    symbol = Column(String, primary_key=True)
    name = Column(String)

    def __init__(self):
        print('Stock initialized...')


class StockPriceDaily(Base):
    __tablename__ = 'price_daily'
    id = Column(Integer, primary_key=True)
    symbol = Column(String, ForeignKey('symbols.symbol'))
    date = Column(Date)
    high = Column(Integer)
    low = Column(Integer)
    open = Column(Integer)
    close = Column(Integer)

    def __init__(self):
        print('Stock Price Daily initialized...')


class StockPriceMinute(Base):
    __tablename__ = 'price_minute'
    id = Column(Integer, primary_key=True)
    symbol = Column(String, ForeignKey('symbols.symbol'))
    datetime = Column(DateTime)
    high = Column(Integer)
    low = Column(Integer)
    open = Column(Integer)
    close = Column(Integer)

    def __init__(self):
        print('Stock Price Minute initialized...')


# Description: Class that retrieves data from the Google Stock Screener.
#              Functonality only implemented as see fit - too many fields to
#              implement all at once.
class GoogleScreener:
    url = 'https://www.google.com/finance'
    market_capital_min = '0'
    market_capital_max = '1T'
    exchange = 'TSE'
    dividend_yield = '3'
    dividend_quarterly_only = True
    last_price = 0
    result_type = 'company'
    sort_by = 'MarketCap'
    result_limit = 200
    offset = 0

    def __init__(self):
        print('Google Screener initialized...')

    # Setters
    def set_market_capital(self, min, max):
        self.market_capital_min = min
        self.market_capital_max = max
        print('Market capital min/max: %s/%s' % self.market_capital_min,
              self.market_capital_max)

    def set_exchange(self, exchange):
        self.exchange = exchange

    def set_dividend_yield(self, dividend_yield):
        self.dividend_yield = dividend_yield

    def set_dividend_quarterly_only(self, flag):
        self.dividend_quarterly_only = flag

    def set_last_price(self, last_price):
        self.last_price = last_price

    def set_sort_by(self, sort_by):
        self.sort_by = sort_by

    def set_result_limit(self, limit):
        self.result_limit = limit

    def set_offset(self, offset):
        self.offset = offset

    # Class methods
    def run(self):
        # build and execute query
        query = ''
        payload = {'output': 'json',
                   'start': self.offset,
                   'num': self.result_limit,
                   'noIL': 1,
                   'restype': self.result_type,
                   'sortas': self.sort_by,
                   'q': query}
        response = requests.get(self.url, params=payload)
        json_response = cjson.decode(response.text)
