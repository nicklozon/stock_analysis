from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, \
    Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
import requests
import cjson


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
    dividend_yield_min = 3
    dividend_yield_max = 0
    last_price_min = 0
    last_price_max = 0
    result_type = 'company'
    sort_by = 'MarketCap'
    result_limit = 200
    offset = 0

    def __init__(self):
        print('Google Screener initialized...')

    # Setters
    def set_market_capital(self, min, max):
        self.market_capital_min = str(min)
        self.market_capital_max = str(max)

    def set_exchange(self, exchange):
        self.exchange = exchange

    def set_dividend_yield_range(self, min, max):
        self.dividend_yield_min = min
        self.dividend_yield_min = max

    def set_last_price_range(self, min, max):
        self.last_price_min = min
        self.last_price_max = max

    def set_sort_by(self, sort_by):
        self.sort_by = sort_by

    def set_result_limit(self, limit):
        self.result_limit = limit

    def set_offset(self, offset):
        self.offset = offset

    # Class methods
    def build_query(self):
        result = '[(exchange == "TSE") & '
        result += '(market_cap >= ' + self.market_capital_min + ') & '
        result += '(market_cap <= ' + self.market_capital_max + ') &'\
            if self.market_capital_max > 0 else ''
        # This may seem redundant (last_price > 0), but it protects from bogus
        # data. It also makes last_price appear in the returned columns.
        result += '(last_price > ' + str(self.last_price_min) + ') & '
        result += '(last_price <= ' + str(self.last_price_max) + ') &'\
            if self.last_price_max > 0 else ''
        result += '(dividend_yield >= ' + str(self.dividend_yield_min) + ') & '
        result += '(dividend_yield <= ' + str(self.dividend_yield_max) + ') &'\
            if self.dividend_yield_max > 0 else ''
        # Again, may seem redundant, but this forces the recent dividend to
        # return in the result. Should be made dynamic in future.
        result += '(dividend_recent_quarter > 0)'
        return result

    def run(self):
        # build and execute query
        payload = {'output': 'json',
                   'start': self.offset,
                   'num': self.result_limit,
                   'noIL': 1,
                   'restype': self.result_type,
                   'sortas': self.sort_by,
                   'q': self.build_query()}
        response = requests.get(self.url, params=payload)
        json_response = cjson.decode(response.text)

        return json_response['searchresults']
