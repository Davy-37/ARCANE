"""Collision-free destination paths."""

import filecmp
from pathlib import Path


def resolve_destination(source: Path, directory: Path) -> Path | None:
    """Choose the path where a file should be copied in a directory.

    Candidates are tried in order: ``name.ext``, ``name_1.ext``,
    ``name_2.ext`` and so on. The first candidate that does not exist is
    returned. If a candidate already exists with the same content as
    `source`, nothing needs to be copied and ``None`` is returned.

    Parameters
    ----------
    source : pathlib.Path
        Path of the existing file to copy.
    directory : pathlib.Path
        Folder that will receive the copy.

    Returns
    -------
    pathlib.Path or None
        A free destination path, or ``None`` if an identical file is already
        present in `directory`.

    Examples
    --------
    >>> import tempfile
    >>> with tempfile.TemporaryDirectory() as folder:
    ...     root = Path(folder)
    ...     source = root / "invoice.pdf"
    ...     _ = source.write_bytes(b"new")
    ...     target = root / "out"
    ...     target.mkdir()
    ...     _ = (target / "invoice.pdf").write_bytes(b"old")
    ...     resolve_destination(source, target).name
    'invoice_1.pdf'
    """
    candidate = directory / source.name
    counter = 0
    while candidate.exists():
        if filecmp.cmp(source, candidate, shallow=False):
            return None
        counter += 1
        candidate = directory / f"{source.stem}_{counter}{source.suffix}"
    return candidate
