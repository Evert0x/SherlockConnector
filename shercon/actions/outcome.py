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

from shercon.abstracts import Action
import shercon.waiters

class Outcome(Action):
    def run(*args, config={}):
        badgerPrice, badgerTokens, bitcoinPrice, bitcoinPremium = args

        tvl = badgerPrice * badgerTokens["formatted"]
        premium = tvl / bitcoinPrice * bitcoinPremium["premium"]

        print("Updating..", premium)
        return shercon.waiters.plugins["Tx"](premium)