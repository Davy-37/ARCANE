"""Folder comparison."""

from ._compare_folders import compare_folders
from ._find_added_files import find_added_files
from ._find_deleted_files import find_deleted_files
from ._find_modified_files import find_modified_files

__all__: list[str] = [
    "find_added_files",
    "find_deleted_files",
    "find_modified_files",
    "compare_folders",
]
