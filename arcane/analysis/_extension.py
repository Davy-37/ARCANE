"""Classification by file extension."""

from pathlib import Path


def by_extension(path: Path) -> str:
    """Return the category name of a file based on its extension.

    The function is pure: it only inspects the name in `path` and never
    touches the disk, so the file does not need to exist.

    Parameters
    ----------
    path : pathlib.Path
        Path of the file to categorize.

    Returns
    -------
    str
        The extension in lowercase and without the leading dot. Only the last
        extension is used, so ``archive.tar.gz`` gives ``"gz"``. Returns
        ``"sans_extension"`` when the file has none, including dotfiles such
        as ``.gitignore``.

    Examples
    --------
    >>> by_extension(Path("budget.XLSX"))
    'xlsx'
    >>> by_extension(Path("Makefile"))
    'sans_extension'
    """
    return path.suffix.lstrip(".").lower() or "sans_extension"
