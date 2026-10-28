"""Classification by modification date."""

from datetime import datetime, timezone
from pathlib import Path


def by_date(path: Path) -> str:
    """Return the modification month of an existing file as ``YYYY-MM``.

    The date read is the last modification time. It is converted using UTC,
    not the local time zone, so the result is the same on every machine: a
    file modified on January 31st at 23:30 UTC is always in January,
    wherever the code runs.

    Parameters
    ----------
    path : pathlib.Path
        Path of the file to categorize.

    Returns
    -------
    str
        The month of the last modification, such as ``"2024-03"``.

    Raises
    ------
    FileNotFoundError
        If `path` does not exist. The error is not caught here: callers
        decide how to report it.

    Examples
    --------
    >>> import os, tempfile
    >>> with tempfile.TemporaryDirectory() as folder:
    ...     note = Path(folder) / "note.txt"
    ...     _ = note.write_bytes(b"x")
    ...     os.utime(note, (1_700_000_000, 1_700_000_000))
    ...     by_date(note)
    '2023-11'
    """
    mtime = path.stat().st_mtime
    return datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m")
