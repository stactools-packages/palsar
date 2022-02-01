from pystac import Link, Provider
# from pystac.extensions.sar import
from pystac.extensions.eo import Band
from pystac.ProviderRole import licensor, processor, producer  # type: ignore

ALOS_PALSAR_PLATFORM = "alos-2/alos"
ALOS_PALSAR_INSTRUMENTS = ["PALSAR-2", "PALSAR"]
ALOS_PALSAR_GSD = 25  # meters
ALOS_PALSAR_EPSG = 4326
ALOS_PALSAR_PROVIDERS = [
    Provider("Japan Aerospace Exploration Agency",
             roles=[producer, processor, licensor],
             url="https://www.eorc.jaxa.jp/ALOS/en/dataset/fnf_e.htm"),
]
ALOS_PALSAR_LINKS = [
    Link(
        "handbook",
        "https://www.eorc.jaxa.jp/ALOS/en/dataset/pdf/DatasetDescription\
            _PALSAR2_Mosaic_FNF_revK.pdf",
        "application/pdf",
        "Global 25 m Resolution PALSAR-2/PALSAR Mosaic and Forest/Non-Forest Map (FNF) \
            Dataset Description",
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
