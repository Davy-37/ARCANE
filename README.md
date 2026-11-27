# ARCANE

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-in%20development-orange)

A Python library to analyze, compare, search, and secure files and folders.
It only relies on the standard library.

> **Status:** early development. Analysis, comparison, search and security features are available;
> the API may still change.

## Features

The library is organized in submodules.

| Submodule | Purpose | Status |
|---|---|---|
| `arcane.analysis` | Classify files into folders by extension, size or date | Available |
| `arcane.comparison` | Detect added, deleted and modified files between folders | Available |
| `arcane.search` | Search files by extension or text content | Available |
| `arcane.security` | Calculate SHA-256 hashes and verify file integrity | Available |

### Analysis

#### File classification

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

### Comparison

The `arcane.comparison` module provides functions to compare two folders
and detect added, deleted and modified files.

| Function | Description |
|---|---|
| `find_added_files()` | Identify files present in the new folder but not in the old folder |
| `find_deleted_files()` | Identify files present in the old folder but not in the new folder |
| `find_modified_files()` | Identify files with the same name but different contents using SHA-256 |
| `compare_folders()` | Combine the three comparison operations |

- Only files directly contained in the folders are compared.
  Subdirectories are ignored.
- Individual comparison functions return sorted lists of filenames.
- `compare_folders()` returns a dictionary containing the selected
  comparison results.
- Comparisons can be enabled or disabled using the `added`, `deleted`
  and `modified` parameters. Disabled comparisons are omitted from the result.
- All functions support the optional `display` parameter, which is
  disabled by default.
- Invalid folder paths raise `FileNotFoundError` or `NotADirectoryError`.

**Example:**

```python
from arcane.comparison import (
    find_added_files,
    find_deleted_files,
    find_modified_files,
    compare_folders,
)

old_folder = "old"
new_folder = "new"

# Individual comparisons
added_files = find_added_files(old_folder, new_folder)
deleted_files = find_deleted_files(old_folder, new_folder)
modified_files = find_modified_files(old_folder, new_folder)

# Compare all differences
result = compare_folders(old_folder, new_folder, display=True)

# Compare only added and modified files
partial_result = compare_folders(old_folder, new_folder, deleted=False)
```

For example, a complete comparison may return:

```python
{
    "added": ["new.txt"],
    "deleted": ["removed.txt"],
    "modified": ["document.txt"],
}
```

When `display=True`, differences are displayed using the following symbols:

- `+`: added file
- `-`: deleted file
- `~`: modified file

### Search

The `arcane.search` module provides functions to search files by extension
or by literal words and phrases in their contents.

| Function | Description |
|---|---|
| `by_extension()` | Find files matching one or more extensions |
| `contains_word()` | Check whether a text file contains a keyword |
| `find_lines()` | Return matching line numbers and contents |
| `count_occurrences()` | Count non-overlapping occurrences |
| `get_context()` | Return matching lines and their surrounding context |
| `search_in_folder()` | Find files containing a keyword, with optional extension filtering |

#### Search by extension

`by_extension()` finds files matching one or more extensions in a directory.

| Parameter | Type | Description |
|---|---|---|
| `root_dir` | `str` or `Path` | Starting directory path |
| `extensions` | `str` or `list[str]` | Target file extension(s) |
| `recursive` | `bool` | Include subdirectories (default: `True`) |

The function returns a list of `Path` objects representing matching files.

- Extensions can be provided with or without a leading dot.
- Multiple extensions can be searched at the same time.
- Extension matching is case-sensitive.
- Directory searches are recursive by default.
- Only files are returned, not directories.
- An empty list is returned if the root path is not a directory
  or no files match.

**Example:**

```python
from arcane.search import by_extension

# Search for a single extension
text_files = by_extension("documents", ".txt")

# Search for multiple extensions
files = by_extension("documents", ["txt", ".pdf", "csv"])

# Search without including subdirectories
local_files = by_extension("documents", "txt", recursive=False)

print(files)
```

#### Search by word

Text searches are case-insensitive by default and support `whole_word=True`
for word-boundary matching. Files are read line by line as UTF-8, ignoring
invalid bytes. This is a plain-text search, not a PDF or Office document parser.
Empty keywords raise `ValueError`; invalid directories return an empty list.
File access errors are propagated. Directory searches are recursive by default.

**Example:**

```python
from arcane.search import count_occurrences, find_lines, search_in_folder

files = search_in_folder("documents", "python", extensions=["txt", "md"])
for file in files:
    print(file, count_occurrences(file, "python"))
    print(find_lines(file, "python"))
```

### Security

The `arcane.security` module provides functions to calculate SHA-256 hashes and detect file modifications by comparing a file's current hash with a reference hash.

- `sha256(path_file)`: Returns the SHA-256 hash of a file as a hexadecimal string.
- `verify_file_integrity(path_file, original_sha256)`: Returns `True` if the file has been modified and `False` if the hashes match.

Files are read in chunks to support large files without loading their entire contents into memory.

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

The following examples demonstrate how to use the main features of ARCANE.

### File classification

Organize files into folders according to their extension, size or date.

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

### Duplicate file detection

Detect, display and optionally remove duplicate files in a folder.

```python
from arcane.analysis import duplicates

# Detect duplicate files
result = duplicates("downloads")
print(result)

# Detect and display duplicate files
duplicates("downloads", display=True)

# Detect, display and remove duplicate files
duplicates("downloads", delete=True, display=True)
```

For example, if `file1.txt` and `file2.txt` have identical contents,
the result is:

```python
[["file1.txt", "file2.txt"]]
```

When `delete=True`, `file1.txt` is kept and `file2.txt` is removed.

> **Warning:** By default, no files are deleted. Use `delete=True` with
> caution, as duplicate files are permanently removed.

### File integrity verification

Calculate the SHA-256 hash of a file and verify whether its contents
have been modified.

```python
from arcane.security import sha256, verify_file_integrity

file_path = "document.txt"

# Calculate the original hash
original_hash = sha256(file_path)
print(original_hash)

# Verify the file's integrity later
is_modified = verify_file_integrity(file_path, original_hash)

if is_modified:
    print("The file has been modified.")
else:
    print("The file has not been modified.")
```

The original hash can be stored as a reference for future integrity checks.

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
