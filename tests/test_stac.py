import os
import unittest
from tempfile import TemporaryDirectory

import pystac
from stactools.testing import TestData

from stactools.palsar import stac
from tests import ALOS2_PALSAR_MOS_FILENAME, test_data


class StacTest(unittest.TestCase):

    def test_create_collection(self):
        # Write tests for each for the creation of a STAC Collection
        # Create the STAC Collection...
        # collection = stac.create_collection()
        # collection.set_self_href("")

        # Check that it has some required attributes
        # self.assertEqual(collection.id, "alos_palsar_mosaic")
        # self.assertEqual(collection.other_attr...

        # Validate
        # collection.validate()
        pass

    def test_create_item(self):
        # Write tests for each for the creation of STAC Items
        # Create the STAC Item...
        with TemporaryDirectory() as tmp_dir:
            test_path = test_data.get_path("data-files/external/")
            cog_path = os.path.join(test_path, [
                d for d in os.listdir(test_path) if d.lower().endswith(".tif")
            ][0])

            # Create stac item
            json_path = os.path.join(tmp_dir, "test.json")
            item = stac.create_item(cog_path)
            item.set_self_href(json_path)
            item.save_object(dest_href=json_path)

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            item_path = os.path.join(tmp_dir, jsons[0])
            item = pystac.read_file(item_path)
            item.validate()

        # Check that it has some required attributes
        # self.assertEqual(item.id, "my-item-id")
        # self.assertEqual(item.other_attr...

        # Validate
        # item.validate()
