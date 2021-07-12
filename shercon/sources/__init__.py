from shercon.abstracts import Source
from shercon.plugins import enumerate_plugins

plugins = enumerate_plugins(
    __file__, "shercon.sources", Source
)
