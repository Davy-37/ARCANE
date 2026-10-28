"""Classification by file size."""

from pathlib import Path

KB = 1024
MB = 1024 * KB

# Upper bounds (inclusive, in bytes) in ascending order; None means no limit.
SIZE_CATEGORIES = (
    (10 * KB, "minuscule"),
    (100 * KB, "petit"),
    (1 * MB, "moyen"),
    (16 * MB, "grand"),
    (128 * MB, "énorme"),
    (None, "gigantesque"),
)


def by_size(path: Path) -> str:
    """Return the size category of an existing file.

    Unlike `by_extension`, this function reads the disk to get the file size.
    Boundaries are inclusive: a file of exactly 10 KB is ``"minuscule"`` and a
    file of 10 KB + 1 byte is ``"petit"``. One KB is 1024 bytes.

    Parameters
    ----------
    path : pathlib.Path
        Path of the file to categorize.

    Returns
    -------
    str
        ``"vide"`` (0 bytes), ``"minuscule"`` (up to 10 KB), ``"petit"`` (up
        to 100 KB), ``"moyen"`` (up to 1 MB), ``"grand"`` (up to 16 MB),
        ``"énorme"`` (up to 128 MB) or ``"gigantesque"`` (anything larger).

    Raises
    ------
    FileNotFoundError
        If `path` does not exist. The error is not caught here: callers
        decide how to report it.

    Examples
    --------
    >>> import tempfile
    >>> with tempfile.TemporaryDirectory() as folder:
    ...     note = Path(folder) / "note.txt"
    ...     _ = note.write_bytes(b"x" * 2048)
    ...     by_size(note)
    'minuscule'
    """
    size = path.stat().st_size
    if size == 0:
        return "vide"
    for limit, name in SIZE_CATEGORIES:
        if limit is None or size <= limit:
            return name
    raise AssertionError(
        "unreachable: the last category has no limit"
    )  # pragma: no cover
