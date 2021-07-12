from decouple import config

from web3 import Web3, HTTPProvider, WebsocketProvider
from web3.middleware import geth_poa_middleware

NETWORK = config('NETWORK')
CHAINID = config('CHAINID', cast=int)

ALCHEMY_TOKEN = config('ALCHEMY_TOKEN')

if NETWORK == 'GOERLI':
    provider = Web3(HTTPProvider("https://eth-goerli.alchemyapi.io/v2/%s" % ALCHEMY_TOKEN))
    provider.middleware_onion.inject(geth_poa_middleware, layer=0)
elif NETWORK == 'MAINNET':
    provider = Web3(HTTPProvider("https://eth-mainnet.alchemyapi.io/v2/%s" % ALCHEMY_TOKEN))
else:
    raise ValueError("Unknown network in .env")