from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, \
    Date, DateTime
from sqlalchemy.ext.declarative import declarative_base


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
    market_capital_min = '0'
    market_capital_max = '1T'
    exchange = 'TSE'
    dividend_yield = '3'
    dividend_quarterly_only = True
    last_price = 0
    restype = 'company'
    sort_by = 'MarketCap'

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
