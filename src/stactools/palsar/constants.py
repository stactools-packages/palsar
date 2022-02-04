from datetime import datetime
from typing import Optional

from pystac import Link, Provider
from pystac import ProviderRole as PR
# from pystac.extensions.sar import
from pystac.extensions.eo import Band
from pystac.utils import str_to_datetime

# TODO: Update if including PALSAR back to 2007

ALOS_COLLECTION_START: Optional[datetime] = str_to_datetime(
    "2015-01-01T00:00:00Z")
ALOS_COLLECTION_END: Optional[datetime] = str_to_datetime(
    "2020-12-31T23:59:59Z")
ALOS_TEMPORAL_EXTENT = [ALOS_COLLECTION_START, ALOS_COLLECTION_END]
ALOS_SPATIAL_EXTENT = [[-180., 90., 180., -90.]]
ALOS_PALSAR_PLATFORMS = ["alos", "alos-2"]
ALOS_PALSAR_INSTRUMENTS = ["PALSAR", "PALSAR-2"]
ALOS_PALSAR_GSD = 25  # meters
ALOS_PALSAR_EPSG = 4326
ALOS_PALSAR_PROVIDERS = [
    Provider("Japan Aerospace Exploration Agency",
             roles=[PR.PRODUCER, PR.PROCESSOR, PR.LICENSOR],
             url="https://www.eorc.jaxa.jp/ALOS/en/dataset/fnf_e.htm"),
    Provider("Microsoft Planetary Computer", roles=[PR.HOST])
]
ALOS_DESCRIPTION = (
    "Global 25 m Resolution PALSAR-2/PALSAR Mosaic and Forest/Non-Forest Map (FNF)"
    "Dataset Description")
ALOS_PALSAR_LINKS = [
    Link("handbook",
         ("https://www.eorc.jaxa.jp/ALOS/en/dataset/pdf/DatasetDescription"
          "_PALSAR2_Mosaic_FNF_revK.pdf"),
         "application/pdf",
         ALOS_DESCRIPTION,
         extra_fields={"description": "Also includes data usage information"})
]
ALOS_PALSAR_BANDS = {
    1:
    Band.create(
        common_name="HH",
        name="HH",
        description="HH polarization backscattering coefficient, 16-bit DN.",
    ),
    2:
    Band.create(
        common_name="HV",
        name="HV",
        description="HV polarization backscattering coefficient, 16-bit DN.",
    ),
    3:
    Band.create(
        common_name="angle",
        name="linci",
        description="Local incidence angle (degrees).",
    ),
    4:
    Band.create(
        common_name="date",
        name="date",
        description="Observation date (days since Jan 1, 1970).",
    ),
    5:
    Band.create(
        common_name="qa",
        name="mask",
        description="Quality Mask",
    ),
    6:
    Band.create(
        name="FNF",
        description="Forest vs Non-Forest classification",
    ),
}
