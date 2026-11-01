import hashlib
from pathlib import Path


def sha256(path_file):
    """
    Calculate the SHA-256 hash of a file.

    Parameters
    ----------
    path_file : str
        Path to the file.

    Returns
    -------
    str
        SHA-256 hash of the file as a hexadecimal string.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    IsADirectoryError
        If the specified path refers to a directory.
    """
    if Path(path_file).is_dir():
        raise IsADirectoryError(f"Expected a file, got a directory: {path_file}")

    file_hash = hashlib.sha256()

    with open(path_file, "rb") as file:
        while True:
            chunk = file.read(8192)

            if not chunk:
                break

            file_hash.update(chunk)

    return file_hash.hexdigest()
