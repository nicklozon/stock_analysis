from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, \
    Date, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
import requests
import cjson


engine = create_engine('postgresql+psycopg2://localhost/stock_analysis',
                       echo=True)
Base = declarative_base()


class Stock(Base):
    __tablename__ = 'symbols'
    symbol = Column(String, primary_key=True)
    name = Column(String)
    active = Column(Boolean)

    def __init__(self, symbol, name, active=True):
        self.symbol = symbol
        self.name = name
        self.active = active | True


class StockPriceDaily(Base):
    __tablename__ = 'price_daily'
    id = Column(Integer, primary_key=True)
    symbol_id = Column(String, ForeignKey('symbols.symbol'))
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
    symbol_id = Column(String, ForeignKey('symbols.symbol'))
    datetime = Column(DateTime)
    high = Column(Integer)
    low = Column(Integer)
    open = Column(Integer)
    close = Column(Integer)

    def __init__(self):
        print('Stock Price Minute initialized...')


# Create the tables
Base.metadata.create_all(engine)


# Description: Class that retricreateves data from the Google Stock Screener.
#              Functonality only implemented as see fit - too many fields to
#              implement all at once.
class GoogleScreener:
    url = 'https://www.google.com/finance'
    market_capital_min = '0'
    market_capital_max = '0'
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
        result += ']'
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

        # Return object
        symbols = []

        # Load the list of stocks using the json response
        for company in json_response['searchresults']:
            # Dynamically load named values into a dictionary
            values = {}
            for column in company['columns']:
                values[column['field']] = column['value']

            # Cast yield, dividend and price
            dividend_yield = float(values['DividendYield']) / 100
            price = float(values['QuoteLast'])
            dividend = float(values['DividendRecentQuarter'])

            # Append stock to symbols if dividend payouts are nore more than
            # quarterly
            if dividend_yield / (dividend / price) < 5:
                symbols.append({'cid': company['id'],
                                'symbol': company['ticker'],
                                'name': company['title']
                                .decode('unicode-escape')}
                               )

        return symbols
