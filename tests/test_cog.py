import os.path
import unittest
from tempfile import TemporaryDirectory

from stactools.palsar import cog
# from stactools.palsar.errors import CogifyError
from tests import ALOS2_PALSAR_MOS_FILENAME, test_data


class CogTest(unittest.TestCase):

    def test_cogify(self):
        # Fix path to data in the package
        path = test_data.get_path(ALOS2_PALSAR_MOS_FILENAME)
        with TemporaryDirectory() as directory:
            cogs = cog.cogify(tile_path=path, output_directory=directory)

            hv_path = cogs[2]
            self.assertEqual(
                os.path.basename(
                    path.replace(".tar.gz", ".tif").replace('MOS', 'sl_HV')),
                os.path.basename(hv_path))

            hh_path = cogs[3]
            self.assertEqual(
                os.path.basename(
                    path.replace(".tar.gz", ".tif").replace('MOS', 'sl_HH')),
                os.path.basename(hh_path))

            linci_path = cogs[0]
            self.assertEqual(
                os.path.basename(
                    path.replace(".tar.gz", ".tif").replace('MOS', 'lini')),
                os.path.basename(linci_path))

            date_path = cogs[4]
            self.assertEqual(
                os.path.basename(
                    path.replace(".tar.gz", ".tif").replace('MOS', 'date')),
                os.path.basename(date_path))

            mask_path = cogs[1]
            self.assertEqual(
                os.path.basename(
                    path.replace(".tar.gz", ".tif").replace('MOS', 'mask')),
                os.path.basename(mask_path))
