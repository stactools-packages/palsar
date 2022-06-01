from datetime import datetime
from typing import Optional

from pystac import Link, Provider, MediaType
from pystac import ProviderRole as PR
from pystac.extensions import sar
from pystac.extensions.item_assets import AssetDefinition
from pystac.extensions.raster import DataType
from pystac.utils import str_to_datetime

# TODO: These values apply to data from 2015 and newer,
# review and adjust if implementing older data.

# Time must be in UTC
ALOS_MOS_COLLECTION_START: Optional[datetime] = str_to_datetime(
    "2015-01-01T00:00:00Z")
ALOS_MOS_COLLECTION_END: Optional[datetime] = str_to_datetime(
    "2020-12-31T23:59:59Z")
ALOS_FNF_COLLECTION_START: Optional[datetime] = str_to_datetime(
    "2015-01-01T00:00:00Z")
ALOS_FNF_COLLECTION_END: Optional[datetime] = str_to_datetime(
    "2016-12-31T23:59:59Z")
ALOS_MOS_TEMPORAL_EXTENT = [ALOS_MOS_COLLECTION_START, ALOS_MOS_COLLECTION_END]
ALOS_FNF_TEMPORAL_EXTENT = [ALOS_FNF_COLLECTION_START, ALOS_FNF_COLLECTION_END]
ALOS_SPATIAL_EXTENT = [[-180., 85., 180., -56.]]
ALOS_PALSAR_PLATFORMS = ["ALOS", "ALOS-2"]
ALOS_PALSAR_INSTRUMENTS = ["PALSAR", "PALSAR-2"]
ALOS_PALSAR_GSD = 25  # meters
ALOS_PALSAR_EPSG = 4326
ALOS_PALSAR_CF = "83.0 dB"
ALOS_PALSAR_PROVIDERS = [
    Provider("Japan Aerospace Exploration Agency",
             roles=[PR.PRODUCER, PR.PROCESSOR, PR.LICENSOR],
             url="https://www.eorc.jaxa.jp/ALOS/en/dataset/fnf_e.htm"),
    Provider("Development Seed",
             roles=[PR.PROCESSOR],
             url="https://developmentseed.org"),
    Provider("Microsoft Planetary Computer",
             roles=[PR.HOST, PR.PROCESSOR],
             url="https://planetarycomputer.microsoft.com/")
]
ALOS_DESCRIPTION = (
    "Global 25 m Resolution PALSAR-2/PALSAR Mosaic and Forest/Non-Forest Map (FNF)"
    "Dataset Description")
ALOS_MOS_DESCRIPTION = "Global 25 m Resolution PALSAR-2/PALSAR Mosaic (MOS)"
ALOS_FNF_DESCRIPTION = "Global 25 m Resolution PALSAR-2/PALSAR Forest/Non-Forest Map (FNF)"
# If you update the Revision(version), also update the handbook link
ALOS_MOS_REVISION = "2.0.0"
ALOS_FNF_REVISION = "2.0.0"

LICENSE_LINK = Link(
    "license",
    "https://earth.jaxa.jp/policy/en.html",
    media_type="text/html",
    title="JAXA Terms of Use of Research Data",
)

ALOS_MOS_LINKS = [
    Link("handbook",
         "https://www.eorc.jaxa.jp/ALOS/en/dataset/pdf/DatasetDescription_PALSAR2_Mosaic_V200.pdf",  # noqa: E501
         "application/pdf",
         ALOS_MOS_DESCRIPTION,
         extra_fields={"description": "Also includes data usage information"}),
    LICENSE_LINK,
]
ALOS_FNF_LINKS = [
    Link("handbook",
         "https://www.eorc.jaxa.jp/ALOS/en/dataset/pdf/DatasetDescription_PALSAR2_FNF_V200.pdf",  # noqa: E501
         "application/pdf",
         ALOS_FNF_DESCRIPTION,
         extra_fields={"description": "Also includes data usage information"}),
    LICENSE_LINK,
]

ALOS_FREQUENCY_BAND = sar.FrequencyBand.L
ALOS_DUAL_POLARIZATIONS = [sar.Polarization.HH, sar.Polarization.HV]
ALOS_QUAD_POLARIZATIONS = [sar.Polarization.HH, sar.Polarization.HV, sar.Polarization.VH, sar.Polarization.VV]
ALOS_PRODUCT_TYPE = "GTC"  # Geometric Terrain Corrected

ALOS_MASK_CLASSIFICATION_CLASSES = [
    {
      "value": 0,
      "name": "no_data",
      "description": "No data"
    },
    {
      "value": 50,
      "name": "water",
      "description": "Water"
    },
    {
      "value": 100,
      "name": "lay_over",
      "description": "Lay over"
    },
    {
      "value": 150,
      "name": "shadowing",
      "description": "Shadowing"
    },
    {
      "value": 255,
      "name": "land",
      "description": "Land"
    }
]
ALOS_FNF_CLASSIFICATION_CLASSES = [
    {
      "value": 0,
      "name": "no_data",
      "description": "No data"
    },
    {
      "value": 1,
      "name": "forest (>90%)",
      "description": "Forest (>90% canopy cover)"
    },
    {
      "value": 2,
      "name": "forest (10-90%)",
      "description": "Forest (10-90% canopy cover)"
    },
    {
      "value": 3,
      "name": "non_forest",
      "description": "Non-forest"
    },
    {
      "value": 4,
      "name": "water",
      "description": "Water"
    },
]

ALOS_MOS_ASSETS = {
    "HH":
    AssetDefinition({
        "title": "HH",
        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
        "description":
        "HH polarization backscattering coefficient, 16-bit DN.",
        "role": "data"
    }),
    "HV":
    AssetDefinition({
        "title": "HV",
        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
        "description":
        "HV polarization backscattering coefficient, 16-bit DN.",
        "role": "data"
    }),
    "VH":
    AssetDefinition({
        "title": "VH",
        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
        "description": "VH polarization backscattering coefficient, 16-bit DN (high-sensitive beam quad-mode only).",
        "role": "data"
    }),
    "VV":
    AssetDefinition({
        "title": "VV",
        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
        "description": "VV polarization backscattering coefficient, 16-bit DN (high-sensitive beam quad-mode only).",
        "role": "data"
    }),
    "linci":
    AssetDefinition({
        "title": "linci",
        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
        "description": "Local incidence angle (degrees).",
        "role": "local-incidence-angle",
    }),
    "date":
    AssetDefinition({
        "title": "date",
        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
        "description": "Observation date (days since Jan 1, 1970).",
        "role": "date"
    }),
    "mask":
    AssetDefinition({
        "title": "mask",
        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
        "description": "Quality Mask",
        "role": "data-mask",
        "raster:bands": [
          {
            "nodata": 0,
            "data_type": "uint8"
          }
        ],
        "classification:classes": ALOS_MASK_CLASSIFICATION_CLASSES,
    }),
    "metadata": AssetDefinition({
        "title": "metadata",
        "type": str(MediaType.XML),
        "description": "Product metadata file",
    })
}

ALOS_FNF_ASSETS = {
    "C":
    AssetDefinition({
        "title": "FNF",
        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
        "description": "Forest vs Non-Forest classification",
        "role": "data",
        "raster:bands": [
          {
            "nodata": 0,
            "data_type": "uint8"
          }
        ],
        "classification:classes": ALOS_FNF_CLASSIFICATION_CLASSES,
    })
}

ALOS_BANDS = {
    "HH": {
        "data_type": DataType.UINT16,
    },
    "HV": {
        "data_type": DataType.UINT16,
    },
    "linci": {
        "data_type": DataType.UINT8,
    },
    "date": {
        "data_type": DataType.UINT16,
    },
    "mask": {
        "data_type": DataType.UINT8,
    },
    "C": {
        "data_type": DataType.UINT8,
    },
}
