"""Result types returned by the classification functions."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple


class CopiedEntry(NamedTuple):
    """A file that was copied.

    Attributes
    ----------
    source : pathlib.Path
        Path of the original file, which is never modified.
    destination : pathlib.Path
        Final path of the copy, after any collision renaming.
    """

    source: Path
    destination: Path


class FailedEntry(NamedTuple):
    """A file that could not be processed.

    Attributes
    ----------
    path : pathlib.Path
        Path of the file that caused the problem.
    reason : str
        Description of what went wrong.
    """

    path: Path
    reason: str


@dataclass
class ClassifyResult:
    """Outcome of a classification run.

    Each instance owns its own lists, so two results never share state.

    Attributes
    ----------
    copied : list of CopiedEntry
        Files that were copied, with their source and final path.
    skipped : list of pathlib.Path
        Files left alone because an identical file already exists at the
        destination.
    failed : list of FailedEntry
        Files that could not be processed, with the reason.

    Examples
    --------
    >>> result = ClassifyResult()
    >>> result.copied, result.skipped, result.failed
    ([], [], [])
    """

    copied: list[CopiedEntry] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)
    failed: list[FailedEntry] = field(default_factory=list)
