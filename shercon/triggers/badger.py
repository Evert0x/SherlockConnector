"""
---
- module: CoingeckoMovingAverage
  args:
  - badger-dao
  - 0.25
- module: TokenAmount
  args:
  - '0x19D97D8fA813EE2f51aD4B4e04EA08bAf4DFfC28'
  - '0x3472A5A71965499acd81997a54BBA8D852C6E53d'
- module: CoingeckoMovingAverage
  args:
  - bitcoin
  - 0.25
- module: SherlockPremium
  args:
  - 'badger.protocol'
  - '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599'
"""

from shercon.abstracts import Trigger

class Badger(Trigger):
    def run(*args, config={}):
        badgerPrice, badgerTokens, bitcoinPrice, bitcoinPremium = args

        tvl = badgerPrice * badgerTokens["formatted"]
        expectedPremium = tvl * bitcoinPremium["percentageBlock"]
        actualPremium = bitcoinPremium["premium"] * bitcoinPrice

        mi = actualPremium - actualPremium * config["deviation"]
        ma = actualPremium + actualPremium * config["deviation"]

        if mi < expectedPremium < ma:
          return False
        return True

