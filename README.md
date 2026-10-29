# ARCANE

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-in%20development-orange)

A Python library to analyze, compare, search, and secure files and folders.
It only relies on the standard library.

> **Status:** early development. Analysis and security features are available;
> the API may still change.

## Features

The library is organized in submodules.

| Submodule | Purpose | Status |
|---|---|---|
| `arcane.analysis` | Classify files into folders by extension, size or date | Available |
| `arcane.comparison` | Compare folders | Planned |
| `arcane.search` | Search files and folders | Planned |
| `arcane.security` | Calculate SHA-256 hashes and verify file integrity | Available |

### Analysis

`File_classify` copies files into one folder per category. The originals are
never modified, and file metadata is kept.

| Criterion | Category | Example |
|---|---|---|
| `"extension"` | Lowercase extension, or `sans_extension` | `pdf`, `jpg` |
| `"size"` | Size range (1 KB = 1024 bytes, upper bounds included) | `minuscule` up to 10 KB, `petit` up to 100 KB, `moyen` up to 1 MB, `grand` up to 16 MB, `énorme` up to 128 MB, `gigantesque` above; `vide` for an empty file |
| `"date"` | Modification month in UTC | `2024-03` |

- A different file with the same name is renamed with a numeric suffix
  (`report_1.pdf`). An identical file is skipped.
- A problem on one file (missing file, permission error) is reported in the
  result and does not stop the others.
- An unknown criterion raises `ValueError` before anything is touched.

### Security

The `arcane.security` module provides functions to calculate SHA-256 hashes and detect file modifications by comparing a file's current hash with a reference hash.

- `sha256(path_file)`: Returns the SHA-256 hash of a file as a hexadecimal string.
- `verify_file_integrity(path_file, original_sha256)`: Returns `True` if the file has been modified and `False` if the hashes match.

Files are read in chunks to support large files without loading their entire contents into memory.

**Example:**

```python
from arcane.security import sha256, verify_file_integrity

file_path = "document.txt"

# Calculate the original hash
original_hash = sha256(file_path)

# Verify the file's integrity later
is_modified = verify_file_integrity(file_path, original_hash)

if is_modified:
    print("The file has been modified.")
else:
    print("The file has not been modified.")
```

Invalid file paths raise appropriate exceptions, such as `FileNotFoundError` or `IsADirectoryError`.

## Installation

Install from the repository:

```bash
pip install git+https://github.com/Davy-37/ARCANE.git
```

For development:

```bash
git clone https://github.com/Davy-37/ARCANE.git
cd ARCANE
pip install -e ".[dev]"
pre-commit install
```

Python 3.10 or newer is required.

## Usage

```python
from pathlib import Path

from arcane.analysis import File_classify

files = [path for path in Path("downloads").iterdir() if path.is_file()]
result = File_classify(files, "extension", Path("sorted"))

for entry in result.copied:
    print(entry.source.name, "->", entry.destination)
print(f"{len(result.skipped)} skipped, {len(result.failed)} failed")
```

With `budget.csv`, `Photo.JPG` and `README` in `downloads/`, the files end up
in `sorted/csv/`, `sorted/jpg/` and `sorted/sans_extension/`.

The result is a `ClassifyResult` with three lists:

- `copied`: entries with `source` and `destination`
- `skipped`: files already present at the destination
- `failed`: entries with `path` and `reason`

The classifiers `by_extension`, `by_size` and `by_date` are also available on
their own, each taking a `Path` and returning the category name.

## Contributing

Contributions, bug reports, and suggestions are welcome. `main` is protected:
every change goes through a pull request linked to an issue. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the workflow.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

## Authors

- Davy Nziengui
- Emilie Théotime
- Jean Novello
