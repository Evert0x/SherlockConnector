from shercon.abstracts import Waiter
from shercon.plugins import enumerate_plugins

plugins = enumerate_plugins(
    __file__, "shercon.waiters", Waiter
)
