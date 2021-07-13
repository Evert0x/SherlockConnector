class Source:
    """Returns a json object"""
    def run(*args):
        pass

class Trigger:
    """Returns as boolean"""
    def run(*args):
        pass

class Action:
    """Doesn't return anything"""
    def run(*args, **kwargs):
        pass

class Waiter:
    """If action is executed, returns waiter class"""

    """Returns boolean to indicate waiting"""
    def verify_done():
        pass