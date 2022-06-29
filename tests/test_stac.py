import os
import unittest
from tempfile import TemporaryDirectory

import pystac
import pytest

from stactools.palsar import cog, stac
from tests import ALOS2_PALSAR_MOS_FILENAME, test_data


class StacTest(unittest.TestCase):

    def test_create_collection(self):
        # Write tests for each for the creation of a STAC Collection
        # Create the STAC Collection...
        collection = stac.create_collection("MOS")
        collection.set_self_href("")

        # Check that it has some required attributes
        self.assertEqual(collection.id, "alos-palsar-mosaic")
        # self.assertEqual(collection.other_attr...

        # Validate
        collection.validate()

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

            # Create stac item
            item = stac.create_item(cogs)
            json_file = '_'.join((os.path.basename(path)).split("_")[0:3])
            json_path = os.path.join(directory, f'{json_file}.json')
            item.validate()
            item.save_object(dest_href=json_path)

            jsons = [p for p in os.listdir(directory) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            item_path = os.path.join(directory, jsons[0])
            print(item_path)
            item = pystac.read_file(item_path)
            item.validate()


def test_mos_ver2():
    import planetary_computer
    item = stac.create_item_from_href(
        "https://pceo.blob.core.windows.net/palsar/v200/alos_palsar_mosaic/2021/N00E070/N00E072_21_F02DAR.xml",  # noqa: E501
        read_href_modifier=planetary_computer.sign
    )
    assert set(item.assets) == {"HH", "HV", "date", "linci", "mask", "metadata"}
    assert item.assets["metadata"].roles == ["metadata"]
    assert "classification:classes" in item.assets["mask"].to_dict()
    item.validate()
    assert item.id == "N00E072_21_F02DAR_MOS"


def test_fnf_ver2():
    import planetary_computer
    item = stac.create_item_from_href(
        "https://pceo.blob.core.windows.net/palsar/v200/alos_fnf_mosaic/2020/N00E005/N00E006_20_C.tif",  # noqa: E501
        read_href_modifier=planetary_computer.sign
    )
    assert set(item.assets) == {"C"}
    assert "classification:classes" in item.assets["C"].to_dict()
    item.validate()
    assert item.id == "N00E006_20_FNF"
    assert item.assets["C"].title == "FNF"


def test_mos_quad():
    import planetary_computer
    item = stac.create_item_from_href(
        "https://pceo.blob.core.windows.net/palsar/v200/alos_palsar_mosaic/2017/N20E140/N20E144_17_FP6QAR.xml",  # noqa: E501
        read_href_modifier=planetary_computer.sign
    )
    assert item.id == "N20E144_17_FP6QAR_MOS"
    assert item.properties["palsar:beam_number"] == "P6"
    assert item.properties["palsar:number_of_polarizations"] == "Q"
    assert item.properties["sar:instrument_mode"] == "F"
    assert item.properties["sat:orbit_state"] == "ascending"
    assert item.properties["sar:observation_direction"] == "right"
    assert set(item.assets) == {
        "date", "linci", "mask", "HH", "HV", "VH", "VV", "metadata"
    }
    assert item.assets["VH"].href == "https://pceo.blob.core.windows.net/palsar/v200/alos_palsar_mosaic/2017/N20E140/N20E144_17_sl_VH_FP6QAR.tif"  # noqa: E501


@pytest.mark.parametrize(["stem", "mode", "beam_number", "polarizations", "orbit", "observation"], [
    ("FP6QAR", "F", "P6", "Q", "A", "R"),
    ("F02DAR", "F", "02", "D", "A", "R"),
    ("U02DDL", "U", "02", "D", "D", "L"),
])
def test_filename_parts(stem, mode, beam_number, polarizations, orbit, observation):
    result = stac.FILENAME_PARTS.match(stem).groupdict()
    assert result["MODE"] == mode
    assert result["BEAM_NUMBER"] == beam_number
    assert result["POLARIZATIONS"] == polarizations
    assert result["ORBIT"] == orbit
    assert result["OBSERVATION"] == observation
