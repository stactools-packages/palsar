import logging
import os
from typing import Dict

import rasterio  # type: ignore
from dateutil.parser import isoparse
from pystac import (Asset, CatalogType, Collection, Extent, Item, Link,
                    MediaType, SpatialExtent, Summaries, TemporalExtent)
from pystac.extensions.item_assets import ItemAssetsExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.raster import RasterBand, RasterExtension
from pystac.extensions.sar import SarExtension
from shapely.geometry import box, mapping  # type: ignore

from stactools.palsar import constants as co

logger = logging.getLogger(__name__)


def create_collection(product: str) -> Collection:
    """Create a STAC Collection

    This function includes logic to extract all relevant metadata from
    an asset describing the STAC collection and/or metadata coded into an
    accompanying constants.py file.

    See `Collection<https://pystac.readthedocs.io/en/latest/api.html#collection>`_.

    Args:
        Product (str): MOS for mosiac, FNF for Forest/Non-Forest

    Returns:
        Item: STAC Item object

    Returns:
        Collection: STAC Collection object
    """
    providers = co.ALOS_PALSAR_PROVIDERS

    extent = Extent(SpatialExtent(co.ALOS_SPATIAL_EXTENT),
                    TemporalExtent([co.ALOS_TEMPORAL_EXTENT]))

    summaries = {
        "platform": co.ALOS_PALSAR_PLATFORMS,
        "instruments": co.ALOS_PALSAR_INSTRUMENTS,
    }

    if product == 'FNF':
        id = "alos_fnf_mosaic"
        title = "ALOS Forest/Non-Forest Annual Mosaic"
        description = co.ALOS_FNF_DESCRIPTION
        keywords = ['ALOS', 'JAXA', 'Forest', 'Land Cover', 'Global']
    else:
        id = "alos_palsar_mosaic"
        title = "ALOS PALSAR Annual Mosaic"
        description = co.ALOS_MOS_DESCRIPTION
        keywords = ['ALOS', 'JAXA', 'Remote Sensing', 'Global']

    collection = Collection(
        id=id,
        title=title,
        description=description,
        license="proprietary",
        providers=providers,
        extent=extent,
        keywords=keywords,
        catalog_type=CatalogType.RELATIVE_PUBLISHED,
        summaries=Summaries(summaries),
        stac_extensions=[
            ItemAssetsExtension.get_schema_uri(),
            SarExtension.get_schema_uri(),
            ProjectionExtension.get_schema_uri(),
            RasterExtension.get_schema_uri(),
        ],
    )

    assets = ItemAssetsExtension.ext(collection, add_if_missing=True)
    if product == 'FNF':
        assets.item_assets = co.ALOS_FNF_ASSETS
    else:
        assets.item_assets = co.ALOS_MOS_ASSETS

    collection.add_links(co.ALOS_PALSAR_LINKS)

    return collection


def create_item(assets_hrefs: Dict, root_href: str = '') -> Item:
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
    year = os.path.basename(asset_href).split("_")[1]
    item_root = '_'.join((os.path.basename(asset_href)).split("_")[0:2])

    with rasterio.open(asset_href) as dataset:
        if dataset.crs.to_epsg() != 4326:
            raise ValueError(
                f"Dataset {asset_href} is not EPSG:4326, which is required for ALOS data"
            )
        bbox = list(dataset.bounds)
        geometry = mapping(box(*bbox))
        transform = list(dataset.transform)
        shape = dataset.shape

    start_datetime = f"20{year}-01-01T00:00:00Z"
    end_datetime = f"20{year}-12-31T23:59:59Z"

    if os.path.basename(asset_href).split("_")[2] == "C":
        item_id = f"{item_root}_FNF"
        properties = {
            "title": item_id,
            "description": "Forest/Non-Forest Classification",
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
        }
        collection = 'alos_fnf_mosaic'
    else:
        item_id = f"{item_root}_MOS"
        properties = {
            "title": item_id,
            "description": "Annual PALSAR Mosaic",
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
        }
        collection = 'alos_palsar_mosaic'

    item = Item(
        id=item_id,
        geometry=geometry,
        bbox=bbox,
        datetime=isoparse(start_datetime),
        properties=properties,
        stac_extensions=[],
    )

    item.collection_id = collection
    item.links.append(
        Link(rel="collection",
             target=os.path.join(root_href, f"{collection}.json")))

    # Data before 2015 is PALSAR, after PALSAR-2
    if int(year) >= 15:
        item.common_metadata.platform = co.ALOS_PALSAR_PLATFORMS[1]
        item.common_metadata.instruments = [co.ALOS_PALSAR_INSTRUMENTS[1]]
    else:
        item.common_metadata.platform = co.ALOS_PALSAR_PLATFORMS[0]
        item.common_metadata.instruments = [co.ALOS_PALSAR_INSTRUMENTS[0]]
    item.common_metadata.gsd = co.ALOS_PALSAR_GSD

    # It is a good idea to include proj attributes to optimize for libs like stac-vrt
    proj_attrs = ProjectionExtension.ext(item, add_if_missing=True)
    proj_attrs.epsg = co.ALOS_PALSAR_EPSG
    proj_attrs.bbox = bbox
    proj_attrs.shape = shape  # Raster shape
    proj_attrs.transform = transform  # Raster GeoTransform

    if os.path.basename(asset_href).split("_")[2] != "C":
        # For MOS product use SAR extension
        sar = SarExtension.ext(item, add_if_missing=True)
        sar.frequency_band = co.ALOS_FREQUENCY_BAND
        sar.polarizations = co.ALOS_POLARIZATIONS
        sar.instrument_mode = co.ALOS_INSTRUMENT_MODE
        sar.product_type = co.ALOS_PRODUCT_TYPE

    # Add an asset to the item (COG for example)
    # For assets in item loop over
    # ["date","xml","linci", "mask", "HH", "HV"]
    for key, value in assets_hrefs.items():
        item.add_asset(
            key,
            Asset(
                # TODO: add relative or absolute url
                href=os.path.join(root_href, os.path.basename(value)),
                media_type=MediaType.COG,
                roles=["data"],
                title=key,
            ),
        )

        cog_asset = item.assets[key]
        raster = RasterExtension.ext(cog_asset, add_if_missing=True)
        raster_band = co.ALOS_BANDS.get(key)
        if raster_band:
            if int(year) >= 19:
                # NoData value changed in 2019 from 0 to 1 for some
                nodata_by_band = {
                    "HH": 1,
                    "HV": 1,
                    "mask": 0,
                    "linci": 1,
                    "date": 1,
                    "C": 0
                }
                nodata = nodata_by_band.get(key, 0)
            else:
                nodata = 0
            raster.bands = [
                RasterBand.create(nodata=nodata,
                                  data_type=raster_band.get('data_type'))
            ]

    return item
