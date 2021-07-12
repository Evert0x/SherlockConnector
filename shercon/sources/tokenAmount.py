import requests

from shercon.config import provider
from shercon.abstracts import Source
import shercon.abi

class TokenAmount(Source):
    def run(*args):
        owner, token = args
        c = provider.eth.contract(address=token, abi=shercon.abi.plugins["erc20"])
        decimals = c.functions.decimals().call()
        raw_amount = c.functions.balanceOf(owner).call()
        return {
            "raw_amount": raw_amount,
            "decimals": decimals,
            "formatted": raw_amount / 10.0 ** decimals
        }