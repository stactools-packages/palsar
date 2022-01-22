import logging

import click

from stactools.palsar import stac
from stactools.palsar import cog

logger = logging.getLogger(__name__)


def create_palsar_command(cli):
    """Creates the stactools-palsar command line utility."""

    @cli.group(
        "palsar",
        short_help=("Commands for working with stactools-palsar"),
    )
    def palsar():
        pass

    @palsar.command(
        "create-collection",
        short_help="Creates a STAC collection",
    )
    @click.argument("destination")
    def create_collection_command(destination: str):
        """Creates a STAC Collection

        Args:
            destination (str): An HREF for the Collection JSON
        """
        collection = stac.create_collection()

        collection.set_self_href(destination)

        collection.save_object()

        return None

    @palsar.command("create-item", short_help="Create a STAC item")
    @click.argument("source")
    @click.argument("destination")
    @click.option(
        "-c",
        "--cogify",
        is_flag=True,
        help="Convert the source into COGs. COG Asset HREFs will be local paths"
    )
    def create_item_command(source: str, destination: str, cogify: bool):
        """Creates a STAC Item

        Args:
            source (str): HREF of the Asset associated with the Item
            destination (str): An HREF for the STAC Collection
            cogify (bool): True/False to convert to COG
        """
        if cogify:
            cogs = cog.cogify(source, destination)
        else:
            cogs = {}
        
        # TODO: pass COGs to create_item, as assets list
        #item = stac.create_item(source)

        #item.save_object(dest_href=destination)

        return None

    return palsar
