"""Find matching lines in text files."""

from pathlib import Path
from typing import List, Tuple, Union

from ._build_pattern import _build_pattern


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
