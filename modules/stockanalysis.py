from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, DateTime
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
