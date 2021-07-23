import os
import json

from decouple import config

from web3 import Web3, HTTPProvider, WebsocketProvider
from web3.middleware import geth_poa_middleware

NETWORK = config('NETWORK')
CHAINID = config('CHAINID', cast=int)

ALCHEMY_TOKEN = config('ALCHEMY_TOKEN')

if NETWORK == 'GOERLI':
    provider = Web3(HTTPProvider("https://eth-goerli.alchemyapi.io/v2/%s" % ALCHEMY_TOKEN))
    provider.middleware_onion.inject(geth_poa_middleware, layer=0)
    sherlock = "0x1291Be112d480055DaFd8a610b7d1e203891C274"
elif NETWORK == 'MAINNET':
    provider = Web3(HTTPProvider("https://eth-mainnet.alchemyapi.io/v2/%s" % ALCHEMY_TOKEN))
    sherlock = "0x1291Be112d480055DaFd8a610b7d1e203891C274"
elif NETWORK == 'LOCALHOST':
    provider = Web3(HTTPProvider("http://127.0.0.1:8545/"))
    sherlock = "0xb7278A61aa25c888815aFC32Ad3cC52fF24fE575"
else:
    raise ValueError("Unknown network in .env")

ADMIN_ADDRESS = config('ADMIN_ADDRESS', default=None)
ADMIN_KEY = config('ADMIN_KEY', default=None)
