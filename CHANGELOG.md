# Changelog

## [v1.2.0] - 2026-06-29

### Added
- CLI interface (`downloadsort`)
- Config-driven file sorting system
- Support for PDFs, Images, Installations, Archives, Documents, Spreadsheets, Presentations, Videos, Music, Code
- Logging system with timestamped actions
- Safe recycle fallback for unknown/invalid files
- Ignore rules support via config.json
- Installable package via pip (`pyproject.toml`)

### Fixed
- Path resolution issues in CLI execution
- Config loading stability in packaged environment

### Notes
- First stable production-ready release