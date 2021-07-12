from shercon.abstracts import Trigger
from shercon.plugins import enumerate_plugins

plugins = enumerate_plugins(
    __file__, "shercon.triggers", Trigger
)
