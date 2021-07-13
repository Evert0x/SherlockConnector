from shercon.abstracts import Waiter

class Tx(Waiter):
    def __init__(self, tx):
        self.tx = tx
        self.counter = 0

    def verify_done(self):
        if self.counter == 8:
            return True
        self.counter += 1

        print("waiting for '%s' to execute" % self.tx)

        return False