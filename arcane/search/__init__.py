"""File and folder search."""

from ._contains_word import contains_word
from ._count_occurrences import count_occurrences
from ._extension import by_extension
from ._find_lines import find_lines
from ._get_context import get_context
from ._search_word import search_in_folder

__all__ = [
    "by_extension",
    "contains_word",
    "count_occurrences",
    "find_lines",
    "get_context",
    "search_in_folder",
]
