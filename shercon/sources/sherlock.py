import requests

from shercon.config import provider, sherlock
from shercon.abstracts import Source
from shercon.misc import identifier

import shercon.abi

class SherlockPremium(Source):
    def run(*args, config={}):
        protocol, token = args
        pid = identifier(protocol)

        c = provider.eth.contract(
            address=sherlock,
            abi=shercon.abi.plugins["sherlock"]
        )
        return c.functions.getProtocolPremium(pid, token).call()

class SherlockPremiumArraySize(Source):
    """Returns amount of tokens protocol uses to pay premiums"""
    def run(*args, config={}):
        protocol, = args
        pid = identifier(protocol)

        return 1