"""Check whether a text file contains a keyword."""

from pathlib import Path
from typing import Union

from ._build_pattern import _build_pattern


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
