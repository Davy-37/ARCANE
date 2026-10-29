from ._sha256 import sha256


def verify_file_integrity(path_file, original_sha256):
    """
    Check whether a file has been modified using its SHA-256 hash.

    Parameters
    ----------
    path_file : str or pathlib.Path
        Path to the file to verify.
    original_sha256 : str
        Reference SHA-256 hash of the original file.

    Returns
    -------
    bool
        True if the file has been modified, False otherwise.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    IsADirectoryError
        If the specified path refers to a directory.
    """
    current_sha256 = sha256(path_file)

    return current_sha256 != original_sha256