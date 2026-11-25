import hashlib
from pathlib import Path


def duplicates(path_folder, delete=False, display=False):
    """
    Detect duplicate files in a folder using SHA-256 hashes.

    Only files directly contained in the folder are analyzed.
    Subdirectories are ignored.

    Parameters
    ----------
    path_folder : str or pathlib.Path
        Path to the folder to analyze.
    delete : bool, optional
        If True, delete duplicate files while keeping one file per group.
        Default is False.
    display : bool, optional
        If True, display duplicate files and deletion operations.
        Default is False.

    Returns
    -------
    list of list of str
        Groups of duplicate filenames, sorted alphabetically.
        Returns an empty list if no duplicates are found.
        When delete=True, returns the groups detected before deletion.

    Raises
    ------
    FileNotFoundError
        If the specified folder does not exist.
    NotADirectoryError
        If the specified path is not a directory.
    """
    folder = Path(path_folder)
    if not folder.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder}")

    if not folder.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {folder}")

    files_by_hash = {}

    for file in folder.iterdir():
        if file.is_file():
            file_hash = hashlib.sha256()
            with open(file, "rb") as f:
                while chunk := f.read(8192):
                    file_hash.update(chunk)
            file_hash = file_hash.hexdigest()
            if file_hash in files_by_hash:
                files_by_hash[file_hash].append(file.name)
            else:
                files_by_hash[file_hash] = []
                files_by_hash[file_hash].append(file.name)

    duplicate_groups = []
    for filenames in files_by_hash.values():
        if len(filenames) > 1:
            duplicate_groups.append(sorted(filenames))

    duplicate_groups.sort()

    if display:
        for group in duplicate_groups:
            print("=")
            for filename in group:
                print(filename)
            print()

    if delete:
        for group in duplicate_groups:
            if display:
                print("delete :")

            for filename in group[1:]:
                file_to_delete = folder / filename
                file_to_delete.unlink()

                if display:
                    print("-", filename)

            if display:
                print()

    return duplicate_groups
