from pathlib import Path


def find_deleted_files(path_old_folder, path_new_folder, display=False):
    """
    Identify files present in the old folder but not in the new folder.

    Only files directly contained in the folders are compared.
    Subdirectories are ignored.

    Parameters
    ----------
    path_old_folder : str or pathlib.Path
        Path to the old folder.
    path_new_folder : str or pathlib.Path
        Path to the new folder.
    display : bool, optional
        If True, display the deleted files.
        Default is False.

    Returns
    -------
    list of str
        Names of deleted files, sorted alphabetically.

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

    diff = old_set - new_set
    result = sorted(diff)

    if display:
        for diff_file in result:
            print("-", diff_file)

    return result
