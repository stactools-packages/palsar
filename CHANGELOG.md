# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). This project attempts to match the major and minor versions of [stactools](https://github.com/stac-utils/stactools) and increments the patch number as needed.

## [Unreleased]

### Added

- STAC item and collection tests
- STAC item and collection generation
- Modified COG generation to pass Asset names to item generation
- Add FNF and MOS data examples to test, since they are normally password protected.
- Implemented handling of NoData in COGs as it differs pre 2017.
- CLI accepts additional HREF root option
- Added Constants for repeatable Metadata
- Added Correction Factor (CF) for correction from Digital Number to Decibels
- Updated to use Revision M data for 2017+
- Handles both zip and tar.gz archives as sources

### Deprecated

- Nothing.

### Removed

- Nothing.

### Fixed

- Nothing.
