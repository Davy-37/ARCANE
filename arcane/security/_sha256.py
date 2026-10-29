import hashlib


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
    """
    file_hash = hashlib.sha256()

    with open(path_file, "rb") as file:
         while True:
            chunk = file.read(8192)

            if not chunk:
                break

            file_hash.update(chunk)

    return file_hash.hexdigest()