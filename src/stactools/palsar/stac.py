import logging
import os
from datetime import datetime, timezone

import rasterio
from pystac import (Asset, CatalogType, Collection, Extent, Item, MediaType,
                    SpatialExtent, TemporalExtent)
from pystac.extensions.projection import ProjectionExtension
from shapely.geometry import box, mapping

from stactools.palsar.constants import (ALOS_PALSAR_EPSG, ALOS_PALSAR_GSD,
                                        ALOS_PALSAR_INSTRUMENTS,
                                        ALOS_PALSAR_LINKS,
                                        ALOS_PALSAR_PLATFORM,
                                        ALOS_PALSAR_PROVIDERS)

logger = logging.getLogger(__name__)

# from pystac import (Asset, CatalogType, Collection, Extent, Item, MediaType,
#                    Provider, ProviderRole, SpatialExtent, TemporalExtent)


def create_collection() -> Collection:
    """Create a STAC Collection

    This function includes logic to extract all relevant metadata from
    an asset describing the STAC collection and/or metadata coded into an
    accompanying constants.py file.

    See `Collection<https://pystac.readthedocs.io/en/latest/api.html#collection>`_.

    Returns:
        Collection: STAC Collection object
    """
    providers = ALOS_PALSAR_PROVIDERS

    # Time must be in UTC
    demo_time = datetime.now(tz=timezone.utc)

    extent = Extent(
        SpatialExtent([[-180., 90., 180., -90.]]),
        TemporalExtent([demo_time, None]),
    )

    collection = Collection(
        # TODO: set in constants
        id="my-collection-id",
        title="A dummy STAC Collection",
        description="Used for demonstration purposes",
        license="CC-0",
        providers=providers,
        extent=extent,
        catalog_type=CatalogType.RELATIVE_PUBLISHED,
    )

    return collection


def create_item(asset_href: str) -> Item:
    """Create a STAC Item

    This function should include logic to extract all relevant metadata from an
    asset, metadata asset, and/or a constants.py file.

    See `Item<https://pystac.readthedocs.io/en/latest/api.html#item>`_.

    Args:
        asset_href (str): The HREF pointing to an asset associated with the item

    Returns:
        Item: STAC Item object
    """

    # For assets in item loop over
    # ["date","xml","linci", "mask", "sl_HH", "sl_HV"]

    with rasterio.open(asset_href) as dataset:
        if dataset.crs.to_epsg() != 4326:
            raise ValueError(
                f"Dataset {asset_href} is not EPSG:4326, which is required for ALOS DEM data"
            )
        bbox = list(dataset.bounds)
        geometry = mapping(box(*bbox))
        transform = dataset.transform
        shape = dataset.shape
    item = Item(id=os.path.splitext(os.path.basename(asset_href))[0],
                geometry=geometry,
                bbox=bbox,
                datetime=datetime.now(tz=timezone.utc),
                properties={},
                stac_extensions={})

    item.add_links(ALOS_PALSAR_LINKS)
    item.common_metadata.platform = ALOS_PALSAR_PLATFORM
    item.common_metadata.instruments = ALOS_PALSAR_INSTRUMENTS
    item.common_metadata.gsd = ALOS_PALSAR_GSD
    item.common_metadata.providers = ALOS_PALSAR_PROVIDERS
    item.common_metadata.license = "proprietary"

    properties = {
        "title": "A dummy STAC Item",
        "description": "Used for demonstration purposes",
    }

    demo_geom = {
        "type":
        "Polygon",
        "coordinates": [[[-180, -90], [180, -90], [180, 90], [-180, 90],
                         [-180, -90]]],
    }

    # Time must be in UTC
    demo_time = datetime.now(tz=timezone.utc)

    item = Item(
        id="my-item-id",
        properties=properties,
        geometry=demo_geom,
        bbox=[-180, 90, 180, -90],
        datetime=demo_time,
        stac_extensions=[],
    )

    # It is a good idea to include proj attributes to optimize for libs like stac-vrt
    proj_attrs = ProjectionExtension.ext(item, add_if_missing=True)
    proj_attrs.epsg = ALOS_PALSAR_EPSG
    proj_attrs.bbox = [-180, 90, 180, -90]
    proj_attrs.shape = shape  # Raster shape
    proj_attrs.transform = transform  # Raster GeoTransform

    # Add an asset to the item (COG for example)
    item.add_asset(
        "image",
        Asset(
            href=asset_href,
            media_type=MediaType.COG,
            roles=["data"],
            title="A dummy STAC Item COG",
        ),
    )

    return item
