from pathlib import Path

from ._find_added_files import find_added_files
from ._find_deleted_files import find_deleted_files
from ._find_modified_files import find_modified_files


def compare_folders(
    path_old_folder,
    path_new_folder,
    added=True,
    deleted=True,
    modified=True,
    display=False,
):
    """
    Compare two folders and return the selected differences.

    Only files directly contained in the folders are compared.
    Subdirectories are ignored.
    Modified files are detected using SHA-256 hashes.

    Parameters
    ----------
    path_old_folder : str or pathlib.Path
        Path to the old folder.
    path_new_folder : str or pathlib.Path
        Path to the new folder.
    added : bool, optional
        If True, detect added files.
        Default is True.
    deleted : bool, optional
        If True, detect deleted files.
        Default is True.
    modified : bool, optional
        If True, detect modified files.
        Default is True.
    display : bool, optional
        If True, display the selected differences.
        Default is False.

    Returns
    -------
    dict of str to list of str
        Comparison results with the keys "added", "deleted",
        and "modified", depending on the selected comparisons.
        Each list contains filenames sorted alphabetically.
        Disabled comparisons are omitted.

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

    result = {}

    if added:
        result_added = find_added_files(path_old_folder, path_new_folder, display)
        result["added"] = result_added

    if deleted:
        result_deleted = find_deleted_files(path_old_folder, path_new_folder, display)
        result["deleted"] = result_deleted

    if modified:
        result_modified = find_modified_files(path_old_folder, path_new_folder, display)
        result["modified"] = result_modified

    return result
