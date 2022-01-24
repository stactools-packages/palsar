import stactools.core

from stactools.palsar.stac import create_collection, create_item

__all__ = ['create_collection', 'create_item']

stactools.core.use_fsspec()


def register_plugin(registry):
    from stactools.palsar import commands
    registry.register_subcommand(commands.create_palsar_command)


__version__ = "0.1.0"
