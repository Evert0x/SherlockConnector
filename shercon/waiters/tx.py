from shercon.abstracts import Waiter

class Tx(Waiter):
    def __init__(self, tx):
        self.tx = tx
        self.counter = 0

    def verify_done(self):
        print("waiting for '%s' to execute" % self.tx)
        # TODO
        # return True if transction receipt is there
        # otherwise return False
        # https://web3py.readthedocs.io/en/stable/web3.eth.html?highlight=receipt#web3.eth.Eth.get_transaction_receipt
        return False