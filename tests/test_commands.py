import os.path
from tempfile import TemporaryDirectory

import pystac
from stactools.testing import CliTestCase, TestData

from stactools.palsar.commands import create_palsar_command

test_data = TestData(__file__)


class CommandsTest(CliTestCase):

    def create_subcommand_functions(self):
        return [create_palsar_command]

    def test_create_collection(self):
        with TemporaryDirectory() as tmp_dir:
            # Run your custom create-collection command and validate

            # Example:
            destination = os.path.join(tmp_dir, "collection.json")

            result = self.run_command(
                ["palsar", "create-collection", destination])

            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            collection = pystac.read_file(destination)
            self.assertEqual(collection.id, "my-collection-id")
            # self.assertEqual(item.other_attr...

            collection.validate()

    def test_create_item(self):
        with TemporaryDirectory() as tmp_dir:
            # Run your custom create-item command and validate
            test_path = test_data.get_path("data-files/")
            cog_path = os.path.join(test_path, [
                d for d in os.listdir(test_path) if d.lower().endswith(".tif")
            ][0])
            # Example:
            # destination = os.path.join(tmp_dir, "item.json")
            result = self.run_command([
                "palsar",
                "create-item",
                cog_path,
                tmp_dir,
            ])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            item = pystac.read_file(jsons[0])
            self.assertEqual(item.id, "my-item-id")
            # self.assertEqual(item.other_attr...

            item.validate()
