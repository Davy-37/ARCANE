import pytest

from arcane.comparison import find_modified_files


def test_modified_files(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "file1.txt").write_text("Hello")
    (tmp_path_new / "file1.txt").write_text("World")

    result = find_modified_files(tmp_path_old, tmp_path_new)

    assert result == ["file1.txt"]


def test_no_modified_files(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "file1.txt").write_text("Hello")
    (tmp_path_new / "file1.txt").write_text("Hello")

    result = find_modified_files(tmp_path_old, tmp_path_new)

    assert result == []


def test_empty_folders(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    result = find_modified_files(tmp_path_old, tmp_path_new)

    assert result == []


def test_sorted_results(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "C.txt").write_text("Old")
    (tmp_path_old / "A.txt").write_text("Old")
    (tmp_path_old / "B.txt").write_text("Old")

    (tmp_path_new / "C.txt").write_text("New")
    (tmp_path_new / "A.txt").write_text("New")
    (tmp_path_new / "B.txt").write_text("New")

    result = find_modified_files(tmp_path_old, tmp_path_new)

    assert result == ["A.txt", "B.txt", "C.txt"]


def test_ignore_subdirectories(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    tmp_subdirectory_old = tmp_path_old / "sub"
    tmp_subdirectory_new = tmp_path_new / "sub"

    tmp_subdirectory_old.mkdir()
    tmp_subdirectory_new.mkdir()

    (tmp_subdirectory_old / "file1.txt").write_text("Hello")
    (tmp_subdirectory_new / "file1.txt").write_text("World")

    result = find_modified_files(tmp_path_old, tmp_path_new)

    assert result == []


def test_ignore_added_and_deleted_files(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "deleted.txt").write_text("Hello")
    (tmp_path_new / "added.txt").write_text("World")

    result = find_modified_files(tmp_path_old, tmp_path_new)

    assert result == []


def test_display(tmp_path, capsys):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "file1.txt").write_text("Hello")
    (tmp_path_new / "file1.txt").write_text("World")

    result = find_modified_files(tmp_path_old, tmp_path_new, True)

    assert result == ["file1.txt"]

    captured = capsys.readouterr()

    assert "~ file1.txt" in captured.out


def test_no_display(tmp_path, capsys):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "file1.txt").write_text("Hello")
    (tmp_path_new / "file1.txt").write_text("World")

    result = find_modified_files(tmp_path_old, tmp_path_new)

    assert result == ["file1.txt"]

    captured = capsys.readouterr()

    assert captured.out == ""


def test_old_folder_not_found(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_new.mkdir()

    with pytest.raises(FileNotFoundError):
        find_modified_files(tmp_path_old, tmp_path_new)


def test_new_folder_not_found(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()

    with pytest.raises(FileNotFoundError):
        find_modified_files(tmp_path_old, tmp_path_new)


def test_old_folder_not_a_directory(tmp_path):
    tmp_path_old = tmp_path / "old.txt"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.write_text("Hello")
    tmp_path_new.mkdir()

    with pytest.raises(NotADirectoryError):
        find_modified_files(tmp_path_old, tmp_path_new)


def test_new_folder_not_a_directory(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new.txt"

    tmp_path_old.mkdir()
    tmp_path_new.write_text("Hello")

    with pytest.raises(NotADirectoryError):
        find_modified_files(tmp_path_old, tmp_path_new)
