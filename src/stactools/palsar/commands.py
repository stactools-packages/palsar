import logging
import os

import click

from stactools.palsar import cog, stac

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
    @click.argument("product")
    @click.argument("destination")
    @click.option("-u",
                  "--url",
                  default='',
                  type=str,
                  help="Root url to prepend to all records")
    def create_collection_command(product: str,
                                  destination: str,
                                  url: str = ''):
        """Creates a STAC Collection

        Args:
            product (str): MOS or FNF Collection type
            destination (str): Path (local or HREF/URL) for the Collection JSON
            url (str): Optional base HREF/URL inside the JSON links
        """
        collection = stac.create_collection(product)
        json_path = os.path.join(destination, f'{collection.id}.json')
        collection.set_self_href(
            os.path.join(url, collection.id, os.path.basename(json_path)))
        collection.validate()
        collection.save_object(dest_href=json_path)

        return None

    @palsar.command("create-item", short_help="Create a STAC item")
    @click.argument("source")
    @click.argument("destination")
    @click.option("-c",
                  "--cogify",
                  is_flag=True,
                  help="Convert the source into COGs.")
    @click.option("-u",
                  "--url",
                  default='',
                  type=str,
                  help="Root HREF/URL to prepend to all records")
    def create_item_command(source: str,
                            destination: str,
                            cogify: bool,
                            url: str = ''):
        """Creates a STAC Item

        Args:
            source (str): HREF of the Asset associated with the Item
            destination (str): An HREF for the STAC Collection
            cogify (bool): Optional True/False to convert to COG
            url (str): Optional base HREF/URL inside the JSON links
        """
        if cogify:
            cogs = cog.cogify(source, destination)
        else:
            cogs = {'cog': source}

        item = stac.create_item(cogs, url)
        json_file = '_'.join((os.path.basename(source)).split("_")[0:3])
        json_path = os.path.join(destination, f'{json_file}.json')
        item.set_self_href(os.path.join(url, os.path.basename(json_path)))
        # TODO: gracefully fail if validate doesn't work
        item.validate()
        item.save_object(dest_href=json_path)

        return cogs

    return palsar
