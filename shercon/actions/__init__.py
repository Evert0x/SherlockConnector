from shercon.abstracts import Action
from shercon.plugins import enumerate_plugins

plugins = enumerate_plugins(
    __file__, "shercon.actions", Action
)
