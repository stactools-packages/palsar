import os
import unittest
from tempfile import TemporaryDirectory

import pystac

from stactools.palsar import cog, stac
from tests import (ALOS2_PALSAR_FNF_FILENAME, ALOS2_PALSAR_MOS_FILENAME,
                   test_data)


class StacTest(unittest.TestCase):

    def test_create_collection(self):
        # Write tests for each for the creation of a STAC Collection
        # Create the STAC Collection...
        collection = stac.create_collection("MOS")
        collection.set_self_href("")

        # Check that it has some required attributes
        self.assertEqual(collection.id, "alos_palsar_mosaic")
        # self.assertEqual(collection.other_attr...

        # Validate
        collection.validate()

    def test_cogify(self):
        # Test a FNF example
        path = test_data.get_path(ALOS2_PALSAR_FNF_FILENAME)
        product = "FNF"
        with TemporaryDirectory() as directory:
            cogs = cog.cogify(tile_path=path, output_directory=directory)

            print(cogs)
            c_path = cogs["C"]
            self.assertEqual(
                os.path.basename(
                    path.replace(".tar.gz", ".tif").replace(product, 'C')),
                os.path.basename(c_path))

    def test_create_item(self):
        # Write tests for each for the creation of STAC Items
        # Create the STAC Item with COG conversion
        # TODO: Test a FNF example
        path = test_data.get_path(ALOS2_PALSAR_MOS_FILENAME)
        product = "MOS"
        with TemporaryDirectory() as directory:
            cogs = cog.cogify(tile_path=path, output_directory=directory)

            print(cogs)
            hv_path = cogs["HV"]
            self.assertEqual(
                os.path.basename(
                    path.replace(".tar.gz", ".tif").replace(product, 'sl_HV')),
                os.path.basename(hv_path))

            hh_path = cogs["HH"]
            self.assertEqual(
                os.path.basename(
                    path.replace(".tar.gz", ".tif").replace(product, 'sl_HH')),
                os.path.basename(hh_path))

            linci_path = cogs["linci"]
            self.assertEqual(
                os.path.basename(
                    path.replace(".tar.gz", ".tif").replace(product, 'linci')),
                os.path.basename(linci_path))

            date_path = cogs["date"]
            self.assertEqual(
                os.path.basename(
                    path.replace(".tar.gz", ".tif").replace(product, 'date')),
                os.path.basename(date_path))

            mask_path = cogs["mask"]
            self.assertEqual(
                os.path.basename(
                    path.replace(".tar.gz", ".tif").replace(product, 'mask')),
                os.path.basename(mask_path))

            # cog_path = os.path.join(directory, [
            #    d for d in os.listdir(directory) if d.lower().endswith(".tif")
            # ][0])

            # Create stac item
            item = stac.create_item(cogs)
            json_file = '_'.join((os.path.basename(path)).split("_")[0:3])
            json_path = os.path.join(directory, f'{json_file}.json')
            # TODO: gracefully fail if validate doesn't work
            item.validate()
            item.save_object(dest_href=json_path)

            jsons = [p for p in os.listdir(directory) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            item_path = os.path.join(directory, jsons[0])
            print(item_path)
            item = pystac.read_file(item_path)
            item.validate()
