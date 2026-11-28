"""Search for keywords in files within a directory."""

from pathlib import Path
from typing import List, Optional, Union

from ._build_pattern import _build_pattern
from ._extension import by_extension


def search_in_folder(
    folder_path: Union[str, Path],
    keyword: str,
    extensions: Optional[Union[str, List[str]]] = None,
    recursive: bool = True,
    ignore_case: bool = True,
    whole_word: bool = False,
) -> List[Path]:
    """
    Find files containing a keyword in a directory.

    Parameters
    ----------
    folder_path : Union[str, Path]
        Directory to search.
    keyword : str
        Literal word or phrase to search for.
    extensions : Optional[Union[str, List[str]]]
        Extensions to filter by, or None to search all files.
        An empty extension filter also searches all files.
    recursive : bool
        Whether to include nested directories.
    ignore_case : bool
        Whether to ignore case.
    whole_word : bool
        Whether to require word boundaries.

    Returns
    -------
    List[Path]
        Paths of matching files, or an empty list for an invalid directory.

    Raises
    ------
    ValueError
        If the keyword is empty.
    OSError
        If a candidate file cannot be opened or read.
    """
    pattern = _build_pattern(keyword, ignore_case, whole_word)
    root = Path(folder_path)
    if not root.is_dir():
        return []

    if extensions:
        files = by_extension(root, extensions, recursive=recursive)
    else:
        entries = root.rglob("*") if recursive else root.iterdir()
        files = [entry for entry in entries if entry.is_file()]

    matching_files = []
    for path in files:
        with path.open(encoding="utf-8", errors="ignore") as file:
            if any(pattern.search(line) for line in file):
                matching_files.append(path)

    return matching_files
