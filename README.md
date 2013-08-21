# Nick's stock analysis scripts

The beginning of my extensive stock analysis scripts. The initial goal, as found in the the current code base, is to provide a an initial series of data to prove a theory of mine - buying a stock during an oversold period (Williams R%) 5 to 10 days prior to an ex-dividend date, then selling at close on the day prior to the ex-dividend date, will typically result in a profit.

Data was selected in two ways: First large market capital stocks on the TSX with a yield >= of 3%, and paying quarterly dividends were slected. Secondly, resource companies were manually removed due to their volatility.

Using the current code base, my findings were an average of 1.075% profit buy and sell. This exceeded my expectations and brings me to the second part of the project, which has not been started yet...

Next Steps
==========
The current code base was not intended to be maintained or extended upon, thus not properly developed form a software point of view.

The next development will include the use of SQLAlchemy (python) ORM to build a constantly running program which will pull 15m delayed data from Yahoo Finance on stocks that are 10 to 5 days away from their ex-dividend date, and compare the pricing trends with the past 14 days to determine if the stocks are beign oversold. If both these criterion are met, the stock information will be posted to a web interface.
