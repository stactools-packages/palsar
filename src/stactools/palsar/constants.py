from pystac import Link, Provider

ALOS_PALSAR_PLATFORM = "alos-2/alos"
ALOS_PALSAR_INSTRUMENTS = ["PALSAR-2", "PALSAR"]
ALOS_PALSAR_GSD = 25  # meters
ALOS_PALSAR_EPSG = 4326
ALOS_PALSAR_PROVIDERS = [
    Provider("Japan Aerospace Exploration Agency",
             roles=["producer", "processor", "licensor"],
             url="https://www.eorc.jaxa.jp/ALOS/en/dataset/fnf_e.htm"),
]
ALOS_PALSAR_LINKS = [
    Link(
        "handbook",
        "https://www.eorc.jaxa.jp/ALOS/en/dataset/pdf/DatasetDescription_PALSAR2_Mosaic_FNF_revK.pdf",
        "application/pdf",
        "Global 25 m Resolution PALSAR-2/PALSAR Mosaic and Forest/Non-Forest Map (FNF) Dataset Description",
        extra_fields={"description": "Also includes data usage information"})
]
ALOS_PALSAR_BANDS = {}
