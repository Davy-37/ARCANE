"""Retrieve matching lines and their surrounding context."""

from collections import deque
from pathlib import Path
from typing import Dict, List, Union

from ._build_pattern import _build_pattern


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
