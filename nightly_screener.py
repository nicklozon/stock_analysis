#!/usr/bin/env python
from modules.stockanalysis import GoogleScreener, Stock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Configure SQLAlchemy engine and session
engine = create_engine('postgresql+psycopg2://localhost/stock_analysis',
                       echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Google Screen for stocks that have >= 3% dividend, and 250MM market cap
gs = GoogleScreener()
gs.exchange = 'TSE'
gs.market_capital_min = '250000000'
gs.market_capital_max = 0
gs.dividend_yield_min = 3
gs.last_price_min = 1
res = gs.run()

# Update all symbols not in list to False
ids = [row['symbol'] for row in res]
session.query(Stock) \
       .filter(Stock.symbol.notin_(ids)) \
       .update({Stock.active: False}, synchronize_session=False)
session.commit()

# UPSERT all records
stocks = [Stock(row['symbol'], row['name']) for row in res]
[session.merge(stock) for stock in stocks]
session.commit()
