"""Search for literal words and phrases in text files."""

import re
from collections import deque
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from ._extension import by_extension


def _build_pattern(keyword: str, ignore_case: bool, whole_word: bool) -> re.Pattern:
    if not keyword:
        raise ValueError("keyword must not be empty")
    flags = re.IGNORECASE if ignore_case else 0
    pattern = rf"\b{re.escape(keyword)}\b" if whole_word else re.escape(keyword)
    return re.compile(pattern, flags)


def contains_word(
    filepath: Union[str, Path],
    keyword: str,
    ignore_case: bool = True,
    whole_word: bool = False,
) -> bool:
    """
    Check whether a text file contains a keyword, stopping at the first match.

    Parameters
    ----------
    filepath : Union[str, Path]
        Path to the file.
    keyword : str
        Literal word or phrase to search for.
    ignore_case : bool
        Whether to ignore case.
    whole_word : bool
        Whether to require word boundaries.

    Returns
    -------
    bool
        True if a matching line exists.

    Raises
    ------
    ValueError
        If the keyword is empty.
    OSError
        If the file cannot be opened or read.
    """
    pattern = _build_pattern(keyword, ignore_case, whole_word)
    with Path(filepath).open(encoding="utf-8", errors="ignore") as file:
        return any(pattern.search(line) for line in file)


def find_lines(
    filepath: Union[str, Path],
    keyword: str,
    ignore_case: bool = True,
    whole_word: bool = False,
) -> List[Tuple[int, str]]:
    """
    Find all lines containing a keyword.

    Parameters
    ----------
    filepath : Union[str, Path]
        Path to the file.
    keyword : str
        Literal word or phrase to search for.
    ignore_case : bool
        Whether to ignore case.
    whole_word : bool
        Whether to require word boundaries.

    Returns
    -------
    List[Tuple[int, str]]
        Matching line numbers (starting at 1) and text without newlines.

    Raises
    ------
    ValueError
        If the keyword is empty.
    OSError
        If the file cannot be opened or read.
    """
    pattern = _build_pattern(keyword, ignore_case, whole_word)
    with Path(filepath).open(encoding="utf-8", errors="ignore") as file:
        return [
            (number, line.rstrip("\n"))
            for number, line in enumerate(file, start=1)
            if pattern.search(line)
        ]


def count_occurrences(
    filepath: Union[str, Path],
    keyword: str,
    ignore_case: bool = True,
    whole_word: bool = False,
) -> int:
    """
    Count non-overlapping occurrences of a keyword in a text file.

    Parameters
    ----------
    filepath : Union[str, Path]
        Path to the file.
    keyword : str
        Literal word or phrase to search for.
    ignore_case : bool
        Whether to ignore case.
    whole_word : bool
        Whether to require word boundaries.

    Returns
    -------
    int
        Total number of occurrences, including multiple matches per line.

    Raises
    ------
    ValueError
        If the keyword is empty.
    OSError
        If the file cannot be opened or read.
    """
    pattern = _build_pattern(keyword, ignore_case, whole_word)
    with Path(filepath).open(encoding="utf-8", errors="ignore") as file:
        return sum(len(pattern.findall(line)) for line in file)


def get_context(
    filepath: Union[str, Path],
    keyword: str,
    lines_around: int = 2,
    ignore_case: bool = True,
    whole_word: bool = False,
) -> List[Dict[str, Union[int, List[str]]]]:
    """
    Return each matching line with its surrounding lines.

    Parameters
    ----------
    filepath : Union[str, Path]
        Path to the file.
    keyword : str
        Literal word or phrase to search for.
    lines_around : int
        Maximum number of lines before and after each matching line.
    ignore_case : bool
        Whether to ignore case.
    whole_word : bool
        Whether to require word boundaries.

    Returns
    -------
    List[Dict[str, Union[int, List[str]]]]
        One dictionary per matching line, with ``line_num`` and ``context``.
        Contexts may overlap if matching lines are close together.

    Raises
    ------
    ValueError
        If the keyword is empty or lines_around is negative.
    OSError
        If the file cannot be opened or read.
    """
    pattern = _build_pattern(keyword, ignore_case, whole_word)
    if lines_around < 0:
        raise ValueError("lines_around must not be negative")

    results = []
    before = deque(maxlen=lines_around)
    pending = deque()

    with Path(filepath).open(encoding="utf-8", errors="ignore") as file:
        for number, line in enumerate(file, start=1):
            clean_line = line.rstrip("\n")

            # Complete the context of earlier matches.
            for _, context in pending:
                context.append(clean_line)

            # Every matching line starts its own context, even if they overlap.
            if pattern.search(line):
                pending.append((number, list(before) + [clean_line]))

            while pending and number - pending[0][0] >= lines_around:
                match_number, context = pending.popleft()
                results.append({"line_num": match_number, "context": context})

            before.append(clean_line)

    # Keep partial contexts when the file ends before all following lines.
    for match_number, context in pending:
        results.append({"line_num": match_number, "context": context})

    return results


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
