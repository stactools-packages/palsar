import logging
import sys

from stactools.testing import TestData

ALOS2_PALSAR_MOS_FILENAME = ("data-files/S16W150_15_MOS_F02DAR.tar.gz")
ALOS2_PALSAR_FNF_FILENAME = ("data-files/S16W150_15_FNF_F02DAR.tar.gz")
ALOS2_PALSAR_MOS_2020_FILENAME = ("data-files/N23W161_20_MOS_F02DAR.tar.gz")

# JAXA data isn't accessible without credentials
# use a local file in the repo instead?
EXTERNAL_DATA = {
    ALOS2_PALSAR_MOS_FILENAME.split('/')[1]: {
        "url": (ALOS2_PALSAR_MOS_FILENAME),
        "compress": "tar.gz",
    },
}

test_data = TestData(__file__, EXTERNAL_DATA)


class TestLogging:
    _set: bool = False

    @staticmethod
    def setup_logging() -> None:
        if not TestLogging._set:
            for package in ["tests", "stactools"]:
                logger = logging.getLogger(package)
                logger.setLevel(logging.INFO)
                formatter = logging.Formatter(
                    "[%(levelname)s] %(asctime)s - %(message)s")

                ch = logging.StreamHandler(sys.stdout)
                ch.setLevel(logging.INFO)
                ch.setFormatter(formatter)
                logger.addHandler(ch)


TestLogging.setup_logging()
