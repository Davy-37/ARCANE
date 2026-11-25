# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/) and the
project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- The `arcane` package, with `arcane.__version__` read from the package
  metadata, and the `analysis`, `comparison`, `search` and `security`
  submodules, each with its own `tests/` folder.
- `File_classify()` to copy files into category folders by extension, size or
  modification month, with the `by_extension()`, `by_size()`, `by_date()` and
  `resolve_destination()` helpers and the `ClassifyResult`, `CopiedEntry` and
  `FailedEntry` result types.
- `duplicates()` to detect files with identical SHA-256 hashes in a folder,
  display duplicate groups, and optionally remove duplicates while keeping one
  copy of each file.
- `sha256()` to compute the SHA-256 hash of a file, and
  `verify_file_integrity()` to check whether a file was modified.
- Pre-commit with Black, Ruff and file checks.
- Issue and pull request templates, and a contributing guide.
- A README describing the features, the installation and a usage example.
