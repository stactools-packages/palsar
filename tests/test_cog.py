import os.path
from tempfile import TemporaryDirectory
import unittest

from stactools.palsar import cog, CogifyError
from tests import ALOS2_PALSAR_MOS_FILENAME, test_data

class CogTest(unittest.TestCase):
    def test_cogify(self):
        # Fix path to data in the package
        path = test_data.get_external_data(ALOS2_PALSAR_MOS_FILENAME)
        with TemporaryDirectory() as directory:
            cogs = cog.cogify(tile_path=path, output_directory=directory)

            hv_path = cogs["sl_HV"]
            self.assertEqual(
                os.path.basename(path.replace(".tar.gz",".tif").replace('MOS', 'sl_HV')),
                os.path.basename(hv_path)
                )

            hh_path = cogs["sl_HH"]
            self.assertEqual(
                os.path.basename(path.replace(".tar.gz",".tif").replace('MOS', 'sl_HH')),
                os.path.basename(hh_path)
            )

            linci_path = cogs["linci"]
            self.assertEqual(
                os.path.basename(path.replace(".tar.gz",".tif").replace('MOS', 'lini')),
                os.path.basename(linci_path)
            )

            date_path = cogs["date"]
            self.assertEqual(
                os.path.basename(path.replace(".tar.gz",".tif").replace('MOS', 'date')),
                os.path.basename(date_path)
            )

            mask_path = cogs["mask"]
            self.assertEqual(
                os.path.basename(path.replace(".tar.gz",".tif").replace('MOS', 'mask')),
                os.path.basename(mask_path)
            )
