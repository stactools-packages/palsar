from datetime import datetime
from typing import Optional

from pystac import Link, Provider
from pystac import ProviderRole as PR
from pystac.extensions import sar
from pystac.extensions.item_assets import AssetDefinition
from pystac.extensions.raster import DataType
from pystac.utils import str_to_datetime

# TODO: These values apply to data from 2015 and newer,
# review and adjust if implementing older data.

# Time must be in UTC
ALOS_COLLECTION_START: Optional[datetime] = str_to_datetime(
    "2015-01-01T00:00:00Z")
ALOS_COLLECTION_END: Optional[datetime] = str_to_datetime(
    "2020-12-31T23:59:59Z")
ALOS_TEMPORAL_EXTENT = [ALOS_COLLECTION_START, ALOS_COLLECTION_END]
ALOS_SPATIAL_EXTENT = [[-180., 90., 180., -90.]]
ALOS_PALSAR_PLATFORMS = ["ALOS", "ALOS-2"]
ALOS_PALSAR_INSTRUMENTS = ["PALSAR", "PALSAR-2"]
ALOS_PALSAR_GSD = 25  # meters
ALOS_PALSAR_EPSG = 4326
ALOS_PALSAR_REVISION = "K"
ALOS_PALSAR_PROVIDERS = [
    Provider("Japan Aerospace Exploration Agency",
             roles=[PR.PRODUCER, PR.PROCESSOR, PR.LICENSOR],
             url="https://www.eorc.jaxa.jp/ALOS/en/dataset/fnf_e.htm"),
    Provider("Microsoft Planetary Computer",
             roles=[PR.HOST, PR.PROCESSOR],
             url="https://planetarycomputer.microsoft.com/")
]
ALOS_DESCRIPTION = (
    "Global 25 m Resolution PALSAR-2/PALSAR Mosaic and Forest/Non-Forest Map (FNF)"
    "Dataset Description")
ALOS_MOS_DESCRIPTION = "Global 25 m Resolution PALSAR-2/PALSAR Mosaic (MOS)"
ALOS_FNF_DESCRIPTION = "Global 25 m Resolution PALSAR-2/PALSAR Forest/Non-Forest Map (FNF)"
ALOS_PALSAR_LINKS = [
    Link("handbook",
         ("https://www.eorc.jaxa.jp/ALOS/en/dataset/pdf/DatasetDescription"
          "_PALSAR2_Mosaic_FNF_revK.pdf"),
         "application/pdf",
         ALOS_DESCRIPTION,
         extra_fields={"description": "Also includes data usage information"}),
    Link("license", "https://earth.jaxa.jp/policy/en.html",
         "JAXA Terms of Use of Research Data")
]

ALOS_FREQUENCY_BAND = sar.FrequencyBand.L
ALOS_POLARIZATIONS = [sar.Polarization.HH, sar.Polarization.HV]
ALOS_INSTRUMENT_MODE = "FBD"  # Fine Beam Dual mode
ALOS_PRODUCT_TYPE = "GTC"  # Geometric Terrain Corrected

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
        "role": "data-mask"
    }),
}

ALOS_FNF_ASSETS = {
    "C":
    AssetDefinition({
        "title": "C",
        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
        "description": "Forest vs Non-Forest classification",
        "role": "data"
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
