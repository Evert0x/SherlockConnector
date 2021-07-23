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
"""

from web3 import Web3
from shercon.config import provider, sherlock, ADMIN_ADDRESS, ADMIN_KEY
from shercon.abstracts import Action

import shercon.abi
import shercon.waiters
from shercon.misc import identifier

class Outcome(Action):
    def run(*args, starg={}, config={}):
        badgerPrice, badgerTokens, bitcoinPrice = args

        tvl = badgerPrice * badgerTokens["formatted"]
        total_premium = tvl / bitcoinPrice * config["premium-rate-block"]
        token_premium = total_premium * config["premium-rate-split"][starg["token"]]

        print("Updating..", token_premium)

        c = provider.eth.contract(
            address=sherlock,
            abi=shercon.abi.plugins["sherlock"]
        )
        data = {
          'chainId': 1337,
          'gas': Web3.toHex(4000000),
          'gasPrice': Web3.toWei('750', 'gwei'),
          'nonce': provider.eth.getTransactionCount(ADMIN_ADDRESS, "pending"),
        }

        print(identifier(starg["protocol"]))
        tx = c.get_function_by_signature(
          'setProtocolPremium(bytes32,address,uint256)'
        )(
          Web3.sha3(text="badger.protocol"), #identifier(starg["protocol"]),
          starg["token"],
          int(token_premium * 10**18)
        ).buildTransaction(data)

        signed_tx = provider.eth.account.signTransaction(tx, private_key=ADMIN_KEY)
        provider.eth.sendRawTransaction(signed_tx.rawTransaction)

        return shercon.waiters.plugins["Tx"](Web3.toHex(signed_tx["hash"]))