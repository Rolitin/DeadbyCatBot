# Changelog

All notable changes to the Dead by Cat Bot project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial setup and configuration for Dead by Cat Bot, a Discord bot designed for Dead by Daylight players.
- Commands for fetching and displaying data (`!shrine`) and checking bot responsiveness (`!ping`).
- Automated updates feature.

### Changed
- Refactored code structure for improved modularity. Moved `functions.py`, `commands.py`, `async_def.py`, and `bot_event.py` into a `main` directory.
- Updated import statements for the new project structure.

### Fixed
- Addressed issues with relative imports in the `main` package.

## [0.1.0] - 2024-02-07
- Initial release of Dead by Cat Bot with basic functionality.
