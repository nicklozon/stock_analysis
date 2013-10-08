#!/opt/virtualenvs/stock_analysis/bin/python
# Description: Collects historical daily stock information on TSX symbols from
#   2010 forward. Stocks are screened using Google's stock screener based on
#   criteria including dividend yield, market capital
#   http captures using requests, json parsing with cjson, postgres database,
#   BeautifulSoup for parsing pages.
import requests
import cjson
import re
import psycopg2
from datetime import datetime
from bs4 import BeautifulSoup
import pdb


# make multiple calls until all data is pulled
def scrape_historical_data():
    rows = []
    while len(rows) % 200 == 0:
        response = requests.get(url, params=payload)

        # Extract the historical table
        soup = BeautifulSoup(response.text)
        table = soup.find('table', class_=re.compile('historical_price'))
        if not table:
            break

        # Check if the table exists, then build a list of rows
        temp = table.find_all('tr')
        temp.pop(0)  # Remove header
        rows.extend(temp)  # Append

        # Prepare for next page, exit loop if number of rows is less than start
        payload['start'] += 200

    # Return the rows
    return rows

# Request the top 250 market capital companies that pay dividends above 3% on
# the TSX
url = 'https://www.google.com/finance'
payload = {'output': 'json', 'start': 0, 'num': 250, 'noIL': 1, 'restype': 'company', 'sortas': 'MarketCap',
           'q': '[(exchange == "TSE") & (market_cap >= 1000000000) & (dividend_yield >= 3) & (dividend_recent_quarter > 0) & (last_price > 0)]'}
response = requests.get(url, params=payload)

# Parse response using cjson
json_response = cjson.decode(response.text)

pdb.set_trace()

# Create list of stocks - [cid, symbol, name]
symbols = []
for company in json_response['searchresults']:
    # Dynamically load named values into a dictionary
    values = {}
    for column in company['columns']:
        values[column['field']] = column['value']

    # Cast yield, dividend and price
    dividend_yield = float(values['DividendYield']) / 100
    price = float(values['QuoteLast'])
    dividend = float(values['DividendRecentQuarter'])

    # Append stock to symbols if dividend payouts are no more than quarterly
    if dividend_yield / (dividend / price) < 5:
        symbols.append({'cid': company['id'], 'symbol': company['ticker'], 'name': company['title'].decode('unicode-escape')})

# Base parameters for historical data requests
url = 'https://www.google.com/finance/historical'
payload = {'startdate': 'Jan 1, 2010', 'enddate': 'Dec 31, 2013', 'num': 200}

# Connect to database
conn = psycopg2.connect("dbname=stock_analysis user=nick")
cur = conn.cursor()

# Download historical data for each stock
for symbol in symbols:
    # set the company id and reset start field
    payload['cid'] = symbol['cid']
    payload['start'] = 0

    # Call the scrape_historical_data function to get get the table rows
    rows = scrape_historical_data()

    # List of characters to remove from the historical data
    bad_chars = '\n,'
    rgx = re.compile('[%s]' % bad_chars)

    # Loop each row and pull the data out
    for row in rows:
        # Scrub data - strip, remove new lines and commas, replace dashes w/ 0
        dt = datetime.strptime(row.contents[1].string.strip(), '%b %d, %Y').date()
        price_open = rgx.sub('', row.contents[2].string.strip()).replace('-', '0.0')
        price_high = rgx.sub('', row.contents[3].string.strip()).replace('-', '0.0')
        price_low = rgx.sub('', row.contents[4].string.strip()).replace('-', '0.0')
        price_close = rgx.sub('', row.contents[5].string.strip())
        volume = rgx.sub('', row.contents[6].string.strip())

        # Insert record
        # TODO: Is there such a thing as a precompiled query? Or is this it?
        cur.execute("INSERT INTO historical_data (symbol, date, price_open, price_high, price_low, price_close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                     (symbol['symbol'], dt, price_open, price_high, price_low, price_close, volume))

    # Commit after each symbol
    conn.commit()

# Close cursor and connection
cur.close()
conn.close()
