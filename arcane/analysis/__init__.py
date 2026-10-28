"""File and folder analysis."""

from arcane.analysis._extension import by_extension
from arcane.analysis._models import ClassifyResult, CopiedEntry, FailedEntry
from arcane.analysis._size import by_size

__all__ = [
    "ClassifyResult",
    "CopiedEntry",
    "FailedEntry",
    "by_extension",
    "by_size",
]
