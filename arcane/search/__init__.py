"""File and folder search."""

from ._extension import by_extension
from ._word import (
    contains_word,
    count_occurrences,
    find_lines,
    get_context,
    search_in_folder,
)

__all__ = [
    "by_extension",
    "contains_word",
    "count_occurrences",
    "find_lines",
    "get_context",
    "search_in_folder",
]
