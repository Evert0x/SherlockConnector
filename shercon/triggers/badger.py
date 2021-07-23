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
  - '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599'
- module: SherlockPremiumArraySize
  args:
  - 'badger.protocol'
"""

from shercon.abstracts import Trigger

class Badger(Trigger):
    def run(*args, starg={}, config={}):
        badgerPrice, badgerTokens, bitcoinPrice, bitcoinPremium, size = args
        assert size == 1, "MISSING_BADGER_TOKEN"
        print(config)
        tvl = badgerPrice * badgerTokens["formatted"]
        expectedPremium = tvl * config["premium-rate-block"]
        actualPremium = bitcoinPremium * bitcoinPrice

        mi = actualPremium - actualPremium * starg["deviation"]
        ma = actualPremium + actualPremium * starg["deviation"]

        if mi < expectedPremium < ma:
          return False
        return True

