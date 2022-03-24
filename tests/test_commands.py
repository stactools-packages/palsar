import os.path
from tempfile import TemporaryDirectory

import pystac
from stactools.testing import CliTestCase

from stactools.palsar.commands import create_palsar_command
from tests import (ALOS2_PALSAR_FNF_FILENAME, ALOS2_PALSAR_MOS_2020_FILENAME,
                   test_data)


class CommandsTest(CliTestCase):

    def create_subcommand_functions(self):
        return [create_palsar_command]

    def test_create_collection(self):
        with TemporaryDirectory() as tmp_dir:
            # Run your custom create-collection command and validate
            destination = os.path.join(tmp_dir, "alos-palsar-mosaic")

            result = self.run_command(
                ["palsar", "create-collection", "MOS", destination])

            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [
                os.path.join(destination, p) for p in os.listdir(destination)
                if p.endswith(".json")
            ]
            self.assertEqual(len(jsons), 1)

            collection = pystac.read_file(jsons[0])
            self.assertEqual(collection.id, "alos-palsar-mosaic")
            # self.assertEqual(item.other_attr...

            collection.validate()

    def test_create_item(self):
        with TemporaryDirectory() as tmp_dir:
            # Run your custom create-item command and validate
            test_path = test_data.get_path(ALOS2_PALSAR_FNF_FILENAME)

            result = self.run_command([
                "palsar",
                "create-item",
                test_path,
                tmp_dir,
                "-c",
            ])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            item = pystac.read_file(os.path.join(tmp_dir, jsons[0]))
            self.assertEqual(item.id, "S16W150_15_FNF")
            # self.assertEqual(item.other_attr...

            item.validate()

    def test_create_item_2020(self):
        with TemporaryDirectory() as tmp_dir:
            # Run create item with cog conversion and override url
            test_path = test_data.get_path(ALOS2_PALSAR_MOS_2020_FILENAME)

            result = self.run_command([
                "palsar",
                "create-item",
                test_path,
                tmp_dir,
                "-c",
                "-u https://foo.bar",
            ])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            item = pystac.read_file(os.path.join(tmp_dir, jsons[0]))
            self.assertEqual(item.id, "N23W161_20_MOS")
            # TODO: Why is there a leading space in href?
            self.assertEqual(item.assets["date"].href.strip(),
                             "https://foo.bar/N23W161_20_date_F02DAR.tif")

            item.validate()
