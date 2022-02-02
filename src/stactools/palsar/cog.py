import logging
import os

from rio_cogeo.cogeo import cog_translate  # type: ignore
from rio_cogeo.profiles import cog_profiles  # type: ignore

# from stactools.palsar.errors import CogifyError
from stactools.palsar.utils import extract_archive, palsar_folder_parse

logger = logging.getLogger(__name__)


def cogify(tile_path: str, output_directory: str):
    """
    Given tile_path to a tile (1x1 degree) folder or tar.gz?
    Convert each band to a COG, save to output_directory
    """

    # Extract tar.gz
    directory = extract_archive(tile_path)
    # If name contains MOS it's mosaic, FNF forest/non
    # FNF is simpler 1 band
    # collect valid data file names
    src_files = palsar_folder_parse(directory)
    # Newer years (2019+) has xml file, ignore
    # Pre 2019, look for .hdr files, then remove hdr for actual file to use
    # for each valid file convert to cog
    cogs = {}
    for variable in src_files:
        # Create a cog filename
        if (not variable.endswith('.tif')):
            cog_name = ".".join([variable, 'tif'])
        else:
            cog_name = variable

        # Extract the Band name
        var_split = variable.split("_")
        if len(var_split) == 5:
            band = var_split[3]
        else:
            band = var_split[2]

        logger.info(f"Creating COG for variable {variable}")
        outfile = os.path.join(output_directory, cog_name)
        infile = os.path.join(directory, variable)

        output_profile = cog_profiles.get("deflate")
        output_profile.update(dict(BIGTIFF="IF_SAFER"))
        output_profile.update({})

        # Dataset Open option (see gdalwarp `-oo` option)
        config = dict(
            GDAL_NUM_THREADS="ALL_CPUS",
            GDAL_TIFF_INTERNAL_MASK=True,
            GDAL_TIFF_OVR_BLOCKSIZE="128",
        )

        cog_translate(
            infile,
            outfile,
            output_profile,
            config=config,
            in_memory=False,
            quiet=True,
        )
        logging.info("Wrote out to " + outfile)

        cogs[band] = outfile

    # return dict of cogs by band
    return cogs
