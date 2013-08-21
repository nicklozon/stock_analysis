-- Description: Calculates the Williams R% metric for each closing price based
--  on the previous 14 days of data.

--UPDATE historical_data SET williams_r = null;
UPDATE historical_data
SET williams_r = t.williams_r
FROM (
		SELECT			hd1.symbol,
								hd1.date,
								CASE
									WHEN (max(hd2.price_high) - min(hd2.price_low)) <> 0 THEN
										((max(hd2.price_high) - hd1.price_close) / (max(hd2.price_high) - min(hd2.price_low)))*-100
									ELSE
										0
								END AS williams_r
		FROM				historical_data hd1
		INNER JOIN 	historical_data hd2
		ON 					hd1.date >= hd2.date
		AND 				hd2.date > (hd1.date - 14)
		AND 				hd1.symbol = hd2.symbol
		AND 				hd2.price_high > 0
		AND 				hd2.price_low > 0
		--WHERE				hd1.symbol = 'TD'
		GROUP BY 		hd1.symbol, hd1.date
		ORDER BY 		hd1.symbol, hd1.DATE ASC
) t
WHERE historical_data.symbol = t.symbol
AND historical_data.date = t.date
