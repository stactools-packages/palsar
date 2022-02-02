import logging
import os
from datetime import datetime, timezone
from typing import Dict

import rasterio  # type: ignore
from pystac import (Asset, CatalogType, Collection, Extent, Item, MediaType,
                    SpatialExtent, TemporalExtent)
from pystac.extensions.projection import ProjectionExtension
from shapely.geometry import box, mapping  # type: ignore

from stactools.palsar.constants import (
    ALOS_DESCRIPTION, ALOS_PALSAR_EPSG, ALOS_PALSAR_GSD,
    ALOS_PALSAR_INSTRUMENTS, ALOS_PALSAR_LINKS, ALOS_PALSAR_PLATFORMS,
    ALOS_PALSAR_PROVIDERS, ALOS_SPATIAL_EXTENT, ALOS_TEMPORAL_EXTENT)

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

    extent = Extent(
        SpatialExtent(ALOS_SPATIAL_EXTENT),
        TemporalExtent(ALOS_TEMPORAL_EXTENT),
    )

    collection = Collection(
        # TODO: set in constants
        id="alos_palsar_mosaic",
        title="ALOS PALSAR Annual Mosaic",
        description=ALOS_DESCRIPTION,
        license="proprietary",
        providers=providers,
        extent=extent,
        catalog_type=CatalogType.RELATIVE_PUBLISHED,
    )

    collection.platform = ALOS_PALSAR_PLATFORMS
    collection.instruments = ALOS_PALSAR_INSTRUMENTS
    collection.gsd = ALOS_PALSAR_GSD
    collection.providers = ALOS_PALSAR_PROVIDERS
    collection.license = "proprietary"

    return collection


def create_item(assets_hrefs: Dict) -> Item:
    """Create a STAC Item

    This function should include logic to extract all relevant metadata from an
    asset, metadata asset, and/or a constants.py file.

    See `Item<https://pystac.readthedocs.io/en/latest/api.html#item>`_.

    Args:
        assets_hrefs (dict): The HREF pointing to an asset associated with the item

    Returns:
        Item: STAC Item object
    """

    # Get the general parameters from the first asset
    asset_href = list(assets_hrefs.values())[0]
    item_id = '_'.join((os.path.basename(asset_href)).split("_")[0:2])
    year = os.path.basename(asset_href).split("_")[1]

    with rasterio.open(asset_href) as dataset:
        if dataset.crs.to_epsg() != 4326:
            raise ValueError(
                f"Dataset {asset_href} is not EPSG:4326, which is required for ALOS DEM data"
            )
        bbox = list(dataset.bounds)
        geometry = mapping(box(*bbox))
        transform = dataset.transform
        shape = dataset.shape

    properties = {
        "title": "A dummy STAC Item",
        "description": "Used for demonstration purposes",
    }

    item = Item(id=item_id,
                geometry=geometry,
                bbox=bbox,
                datetime=datetime.now(tz=timezone.utc),
                properties=properties,
                stac_extensions=[])

    item.add_links(ALOS_PALSAR_LINKS)

    # Data before 2015 is PALSAR, after PALSAR-2
    if year >= 15:
        item.common_metadata.platform = ALOS_PALSAR_PLATFORMS[1]
        item.common_metadata.instruments = ALOS_PALSAR_INSTRUMENTS[1]
    item.common_metadata.gsd = ALOS_PALSAR_GSD
    item.common_metadata.providers = ALOS_PALSAR_PROVIDERS
    item.common_metadata.license = "proprietary"

    # It is a good idea to include proj attributes to optimize for libs like stac-vrt
    proj_attrs = ProjectionExtension.ext(item, add_if_missing=True)
    proj_attrs.epsg = ALOS_PALSAR_EPSG
    proj_attrs.bbox = bbox
    proj_attrs.shape = shape  # Raster shape
    proj_attrs.transform = transform  # Raster GeoTransform

    # Add an asset to the item (COG for example)
    # For assets in item loop over
    # ["date","xml","linci", "mask", "sl_HH", "sl_HV"]
    for key, value in assets_hrefs.items():
        item.add_asset(
            key,
            Asset(
                # TODO: add relative or absolute url
                href=os.path.basename(value),
                media_type=MediaType.COG,
                roles=["data"],
                title=key,
            ),
        )

    return item
