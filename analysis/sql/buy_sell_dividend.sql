-- Description: Captures close price when williams_r is oversold, then captures
--   close price prior to ex-dividend date. Simulate buy and sell on the 
--   respective prices and calculate the profit %.

--SELECT	hd.symbol,
--        hd.date,
--				hd2.date,
--				hd.price_close as buy,
--				hd2.price_close as sell,
--				(hd2.price_close - hd.price_close) / hd.price_close * 100 as profit
SELECT hd.symbol, avg((hd2.price_close - hd.price_close) / hd.price_close * 100)
FROM historical_data hd
INNER JOIN (
	SELECT hd.symbol, ed.date as eddate, min(hd.date) as date
	FROM ex_dividend_data ed
	INNER JOIN historical_data hd
	ON ed.symbol = hd.symbol
	AND hd.date between (ed.date - 14) and (ed.date - 7)
	AND hd.williams_r <= -80
	GROUP BY hd.symbol, ed.date
	ORDER BY hd.symbol, ed.date
) t
ON hd.symbol = t.symbol
AND hd.date = t.date
INNER JOIN historical_data hd2
ON hd.symbol = hd2.symbol
INNER JOIN (
	SELECT hd.symbol, ed.date as eddate, max(hd.date) as date
	FROM historical_data hd
	INNER JOIN ex_dividend_data ed
	ON hd.symbol = ed.symbol
	AND hd.date < ed.date
	GROUP BY hd.symbol, ed.date
	ORDER BY hd.symbol, ed.date
) t2
ON hd2.symbol = t2.symbol
AND hd2.date = t2.date
AND t.eddate = t2.eddate
-- Following values are hard coded STD DEV at the time of running
--   Removing outliers greatly affects the result, more accurate.
WHERE ((hd2.price_close - hd.price_close) / hd.price_close * 100) <= 11.25021228544331
and ((hd2.price_close - hd.price_close) / hd.price_close * 100) >= -8.30569185140395
GROUP BY hd.symbol
--ORDER BY avg((hd2.price_close - hd.price_close) / hd.price_close * 100) ASC
ORDER BY hd2.date ASC
