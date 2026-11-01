from pathlib import Path
from typing import List, Union


def by_extension(
    root_dir: Union[str, Path],
    extensions: Union[str, List[str]],
    recursive: bool = True,
) -> List[Path]:
    """
    Find files matching specific extensions in a directory.

    Parameters
    ----------
    root_dir : Union[str, Path]
        Starting directory path.
    extensions : Union[str, List[str]]
        Target extension(s), e.g. ``'.txt'`` or ``['txt', '.csv']``.
    recursive : bool
        Whether to search nested directories.

    Returns
    -------
    List[Path]
        Paths of all matching files.
    """
    root_path = Path(root_dir)
    if not root_path.is_dir():
        return []

    if isinstance(extensions, str):
        extensions = [extensions]
    valid_exts = {ext if ext.startswith(".") else f".{ext}" for ext in extensions}

    files = root_path.rglob("*") if recursive else root_path.iterdir()
    return [file for file in files if file.is_file() and file.suffix in valid_exts]
