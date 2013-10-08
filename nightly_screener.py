#!/usr/bin/env python
from modules.stockanalysis import GoogleScreener
import pdb


gs = GoogleScreener()
gs.market_capital_min = '250000000'
gs.market_capital_max = 0
res = gs.run()

pdb.set_trace()
