import pytest

from arcane.comparison import find_deleted_files


def test_deleted_files(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "file1.txt").write_text("Hello")

    result = find_deleted_files(tmp_path_old, tmp_path_new)

    assert result == ["file1.txt"]


def test_no_deleted_files(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "file1.txt").write_text("Hello")
    (tmp_path_new / "file1.txt").write_text("Hello")

    result = find_deleted_files(tmp_path_old, tmp_path_new)

    assert result == []


def test_empty_folders(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    result = find_deleted_files(tmp_path_old, tmp_path_new)

    assert result == []


def test_sorted_results(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "file1.txt").write_text("Hello")
    (tmp_path_old / "C.txt").write_text("C")
    (tmp_path_old / "A.txt").write_text("A")
    (tmp_path_old / "B.txt").write_text("B")
    (tmp_path_new / "file1.txt").write_text("Hello")

    result = find_deleted_files(tmp_path_old, tmp_path_new)

    assert result == ["A.txt", "B.txt", "C.txt"]


def test_ignore_subdirectories(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    tmp_subdirectorie_new = tmp_path_new / "sub"
    tmp_subdirectory_old = tmp_path_old / "sub"

    tmp_subdirectorie_new.mkdir()
    tmp_subdirectory_old.mkdir()

    (tmp_path_old / "file1.txt").write_text("Hello")
    (tmp_path_new / "file1.txt").write_text("Hello")
    (tmp_subdirectorie_new / "C.txt").write_text("C")
    (tmp_subdirectory_old / "D.txt").write_text("D")

    result = find_deleted_files(tmp_path_old, tmp_path_new)

    assert result == []


def test_display(tmp_path, capsys):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "file1.txt").write_text("Hello")
    (tmp_path_old / "file2.txt").write_text("World")
    (tmp_path_new / "file1.txt").write_text("Hello")

    result = find_deleted_files(tmp_path_old, tmp_path_new, True)

    assert result == ["file2.txt"]

    captured = capsys.readouterr()

    assert "- file2.txt" in captured.out


def test_no_display(tmp_path, capsys):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "file1.txt").write_text("Hello")
    (tmp_path_old / "file2.txt").write_text("World")
    (tmp_path_new / "file1.txt").write_text("Hello")

    result = find_deleted_files(tmp_path_old, tmp_path_new, False)

    assert result == ["file2.txt"]

    captured = capsys.readouterr()

    assert captured.out == ""


def test_old_folder_not_found(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_new.mkdir()

    with pytest.raises(FileNotFoundError):
        find_deleted_files(tmp_path_old, tmp_path_new)


def test_new_folder_not_found(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()

    with pytest.raises(FileNotFoundError):
        find_deleted_files(tmp_path_old, tmp_path_new)


def test_old_folder_not_a_directory(tmp_path):
    tmp_path_old = tmp_path / "old.txt"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.write_text("Hello")
    tmp_path_new.mkdir()

    with pytest.raises(NotADirectoryError):
        find_deleted_files(tmp_path_old, tmp_path_new)


def test_new_folder_not_a_directory(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new.txt"

    tmp_path_old.mkdir()
    tmp_path_new.write_text("Hello")

    with pytest.raises(NotADirectoryError):
        find_deleted_files(tmp_path_old, tmp_path_new)
