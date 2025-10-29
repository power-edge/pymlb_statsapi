# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] - 2025-07-20
### Added
- Utility functions for schema loading in `schema_loader`.

### Changed
- Revised singleton `EndpointConfig` for endpoint configuration to add schema_loader arg.
- Cleanup of old configs path functionality

### Fixed
- Resolved `ModuleNotFoundError` for `pymlb_statsapi` during build.

## [<=0.1.2] - 2025-07-19
### Added
- Initial project setup with `setup.py` and `setup.cfg`.
- Basic structure for `pymlb_statsapi` package.
- `bumpversion` configuration for version management.
