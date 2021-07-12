import requests
import sha3

from shercon.config import provider
from shercon.abstracts import Source
import shercon.abi

class SherlockPremium(Source):
    def run(*args):
        protocol, token = args

        k = sha3.keccak_256()
        k.update(protocol.encode())

        identifier = k.hexdigest()
        # TODO, contract calls to get current premium
        return {
            "premium": 0.00000006,
            "percentageYear": 0.01,
            "percentageBlock": 0.000000004
        }