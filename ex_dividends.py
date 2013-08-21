#!/usr/bin/env python
# Description: Pulls historical ex-dividend dates from yahoo stocks
import requests
import psycopg2
from datetime import datetime
from bs4 import BeautifulSoup


# Connect to database
conn = psycopg2.connect("dbname=stock_analysis user=nick")
cur1 = conn.cursor()
cur2 = conn.cursor()

cur1.execute('SELECT DISTINCT symbol FROM historical_data')
counter = 0
for symbol in cur1:
    url = 'http://finance.yahoo.com/q/hp'
    counter = counter + 1
    print counter, symbol[0]
    payload = {'s': symbol[0].replace('.', '-') + '.TO', 'a': 0, 'b': 1, 'c': 2010, 'd': 11, 'e': 31, 'f': 2013, 'g': 'v'}
    response = requests.get(url, params=payload)

    soup = BeautifulSoup(response.text)
    cells = soup.find_all('td', class_='yfnc_tabledata1')

    even = [x * 2 for x in range(len(cells) / 2)]
    for x in even:
        date = datetime.strptime(cells[x].string, '%b %d, %Y').date()
        cur2.execute('INSERT INTO ex_dividend_data (symbol, date) VALUES (%s, %s)', (symbol[0], date))

    # Commit after each symbol
    conn.commit()

# Close cursor and connection
cur1.close()
cur2.close()
conn.close()
