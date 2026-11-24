import hashlib
from pathlib import Path


def find_modified_files(path_old_folder, path_new_folder, display=False):
    """
    Identify files with the same name but different contents.

    File contents are compared using SHA-256 hashes.
    Only files directly contained in the folders are compared.
    Subdirectories are ignored.

    Parameters
    ----------
    path_old_folder : str or pathlib.Path
        Path to the old folder.
    path_new_folder : str or pathlib.Path
        Path to the new folder.
    display : bool, optional
        If True, display the modified files.
        Default is False.

    Returns
    -------
    list of str
        Names of modified files, sorted alphabetically.

    Raises
    ------
    FileNotFoundError
        If either folder does not exist.
    NotADirectoryError
        If either path is not a directory.
    """
    old_folder = Path(path_old_folder)
    new_folder = Path(path_new_folder)

    for folder in (old_folder, new_folder):
        if not folder.exists():
            raise FileNotFoundError(f"Folder does not exist: {folder}")

        if not folder.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {folder}")

    old_set = set()
    new_set = set()

    for file in old_folder.iterdir():
        if file.is_file():
            old_set.add(file.name)

    for file in new_folder.iterdir():
        if file.is_file():
            new_set.add(file.name)

    common_files = set.intersection(old_set, new_set)

    modified = set()

    for file in common_files:
        path_old_file = old_folder / file
        path_new_file = new_folder / file

        with open(path_old_file, "rb") as old_file:
            old_content = old_file.read()
            old_file_hash = hashlib.sha256(old_content).hexdigest()

        with open(path_new_file, "rb") as new_file:
            new_content = new_file.read()
            new_file_hash = hashlib.sha256(new_content).hexdigest()

        if old_file_hash != new_file_hash:
            modified.add(file)

    result = sorted(modified)

    if display:
        for modified_file in result:
            print("~", modified_file)

    return result
