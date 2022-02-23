[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/stactools-packages/stactools-palsar/main?filepath=docs/installation_and_basic_usage.ipynb)

# stactools-palsar

- Name: stactools-palsar
- Package: `stactools.palsar`
- PyPI: https://pypi.org/project/stactools-palsar/
- Owner: @githubusername
- Dataset homepage: http://example.com
- STAC extensions used:
  - [proj](https://github.com/stac-extensions/projection/)
- Extra fields:
  - `stactools-palsar:custom`: A custom attribute

This package converts ALOS/ALOS-2 PALSAR/PALSAR-2 annual mosaic or forest/non-forest mosaic tar.gz tiles into STAC items with an optional conversion to cloud optimized geotiff (COG). You can then create accompanying STAC collections for annual mosaic (alos_plasar_mosaic) or forest/non-forest (alos_fnf_mosaic).

## Examples

### STAC objects

- [Collection](examples/collection.json)
- [Item](examples/item/item.json)

### Command-line usage

Description of the command line functions

```bash
$ stac stactools-palsar create-item source destination -h href -c
$ stac palsar create-collection MOS tests/data-files/ -h https://my_catalog_url.io
$ stac palsar create-item tests/data-files/S16W150_15_FNF_F02DAR.tar.gz tests/data-files -h https://my_catalog_url.io/alos_fnf_mosaic/ -c
```

Use `stac stactools-palsar --help` to see all subcommands and options.
