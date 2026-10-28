"""Copy files into category folders."""

import shutil
from collections.abc import Callable, Iterable
from pathlib import Path

from arcane.analysis._date import by_date
from arcane.analysis._destination import resolve_destination
from arcane.analysis._extension import by_extension
from arcane.analysis._models import ClassifyResult, CopiedEntry, FailedEntry
from arcane.analysis._size import by_size

CRITERIA: dict[str, Callable[[Path], str]] = {
    "extension": by_extension,
    "size": by_size,
    "date": by_date,
}

DEFAULT_DEST_NAME = "classified"


def File_classify(
    files: Iterable[Path],
    criterion: str,
    dest_root: Path | None = None,
) -> ClassifyResult:
    """Copy each file into ``dest_root/<category>/`` according to a criterion.

    Files are copied with their metadata. The originals are never modified.
    Category folders are created when missing and reused otherwise.

    If a file with the same name but a different content already exists, the
    copy is renamed with a numeric suffix (``report_1.pdf``). If an identical
    file is already present, the file is skipped. A problem on one file, such
    as a missing file or a permission error, is recorded in the result and
    the processing continues with the next file.

    Parameters
    ----------
    files : iterable of pathlib.Path
        Paths of the files to classify.
    criterion : {"extension", "size", "date"}
        How the category of each file is computed.
    dest_root : pathlib.Path, optional
        Root folder that receives the category folders. Defaults to a
        ``classified`` folder in the current directory.

    Returns
    -------
    ClassifyResult
        The ``copied`` files (source and final path), the ``skipped`` files
        (already present) and the ``failed`` files (path and reason).

    Raises
    ------
    ValueError
        If `criterion` is unknown. It is raised before any file or folder is
        touched.

    Examples
    --------
    >>> import tempfile
    >>> with tempfile.TemporaryDirectory() as folder:
    ...     root = Path(folder)
    ...     source = root / "budget.csv"
    ...     _ = source.write_bytes(b"a,b")
    ...     result = File_classify([source], "extension", root / "out")
    ...     result.copied[0].destination.relative_to(root).as_posix()
    'out/csv/budget.csv'
    """
    try:
        categorize = CRITERIA[criterion]
    except KeyError:
        valid = ", ".join(sorted(CRITERIA))
        raise ValueError(
            f"Unknown criterion {criterion!r}; expected one of: {valid}"
        ) from None

    root = Path(dest_root) if dest_root is not None else Path.cwd() / DEFAULT_DEST_NAME
    result = ClassifyResult()

    for source in map(Path, files):
        try:
            directory = root / categorize(source)
            directory.mkdir(parents=True, exist_ok=True)
            destination = resolve_destination(source, directory)
            if destination is None:
                result.skipped.append(source)
                continue
            shutil.copy2(source, destination)
            result.copied.append(CopiedEntry(source, destination))
        except OSError as error:
            result.failed.append(FailedEntry(source, str(error)))

    return result
