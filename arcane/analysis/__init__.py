"""File and folder analysis."""

from arcane.analysis._classify import File_classify
from arcane.analysis._date import by_date
from arcane.analysis._destination import resolve_destination
from arcane.analysis._duplicates import duplicates
from arcane.analysis._extension import by_extension
from arcane.analysis._models import ClassifyResult, CopiedEntry, FailedEntry
from arcane.analysis._size import by_size

__all__: list[str] = [
    "ClassifyResult",
    "CopiedEntry",
    "duplicates",
    "FailedEntry",
    "File_classify",
    "by_date",
    "by_extension",
    "by_size",
    "resolve_destination",
]
