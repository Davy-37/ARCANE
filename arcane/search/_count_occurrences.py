"""Count keyword occurrences in text files."""

from pathlib import Path
from typing import Union

from ._build_pattern import _build_pattern


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
