import pytest

from arcane.analysis import duplicates


def test_duplicates_basic(tmp_path):
    (tmp_path / "file1.txt").write_text("Hello")
    (tmp_path / "file2.txt").write_text("Hello")
    (tmp_path / "file3.txt").write_text("World")

    result = duplicates(tmp_path)

    assert result == [["file1.txt", "file2.txt"]]


def test_no_duplicates(tmp_path):
    (tmp_path / "file1.txt").write_text("Hello")
    (tmp_path / "file2.txt").write_text("Cat")
    (tmp_path / "file3.txt").write_text("World")

    result = duplicates(tmp_path)

    assert result == []


def test_empty_folder(tmp_path):

    result = duplicates(tmp_path)

    assert result == []


def test_multiple_groups(tmp_path):
    (tmp_path / "file1.txt").write_text("Hello")
    (tmp_path / "file2.txt").write_text("Hello")
    (tmp_path / "file3.txt").write_text("World")
    (tmp_path / "file4.txt").write_text("World")
    (tmp_path / "file5.txt").write_text("World")
    (tmp_path / "file6.txt").write_text("Cat")

    result = duplicates(tmp_path)

    assert result == [
        ["file1.txt", "file2.txt"],
        ["file3.txt", "file4.txt", "file5.txt"],
    ]


def test_ignore_subdirectories(tmp_path):
    (tmp_path / "file1.txt").write_text("Hello")
    (tmp_path / "file2.txt").write_text("Hello")
    (tmp_path / "hello").mkdir()
    (tmp_path / "hello" / "filehello.txt").write_text("Hello")
    (tmp_path / "file3.txt").write_text("World")
    (tmp_path / "file4.txt").write_text("World")
    (tmp_path / "file5.txt").write_text("World")
    (tmp_path / "file6.txt").write_text("Cat")

    result = duplicates(tmp_path)

    assert result == [
        ["file1.txt", "file2.txt"],
        ["file3.txt", "file4.txt", "file5.txt"],
    ]


def test_delete_false(tmp_path):
    (tmp_path / "file1.txt").write_text("Hello")
    (tmp_path / "file2.txt").write_text("Hello")
    (tmp_path / "file3.txt").write_text("World")

    result = duplicates(tmp_path, False)

    assert result == [["file1.txt", "file2.txt"]]
    assert (tmp_path / "file1.txt").exists()
    assert (tmp_path / "file2.txt").exists()
    assert (tmp_path / "file3.txt").exists()


def test_delete_true(tmp_path):
    (tmp_path / "file1.txt").write_text("Hello")
    (tmp_path / "file2.txt").write_text("Hello")
    (tmp_path / "file3.txt").write_text("World")

    result = duplicates(tmp_path, True)

    assert result == [["file1.txt", "file2.txt"]]
    assert (tmp_path / "file1.txt").exists()
    assert not (tmp_path / "file2.txt").exists()
    assert (tmp_path / "file3.txt").exists()


def test_folder_not_found(tmp_path):
    folder = tmp_path / "unknown"

    with pytest.raises(FileNotFoundError):
        duplicates(folder)


def test_not_a_directory(tmp_path):
    file = tmp_path / "hello.txt"
    file.write_text("Hello")

    with pytest.raises(NotADirectoryError):
        duplicates(file)


def test_display_true(tmp_path, capsys):
    (tmp_path / "file1.txt").write_text("Hello")
    (tmp_path / "file2.txt").write_text("Hello")
    (tmp_path / "file3.txt").write_text("World")

    duplicates(tmp_path, display=True)

    captured = capsys.readouterr()

    assert "file1.txt" in captured.out
    assert "file2.txt" in captured.out
    assert "file3.txt" not in captured.out


def test_delete_and_display(tmp_path, capsys):
    (tmp_path / "file1.txt").write_text("Hello")
    (tmp_path / "file2.txt").write_text("Hello")
    (tmp_path / "file3.txt").write_text("World")

    result = duplicates(tmp_path, delete=True, display=True)

    captured = capsys.readouterr()

    assert "file1.txt" in captured.out
    assert "file2.txt" in captured.out
    assert "file3.txt" not in captured.out
    assert "delete :" in captured.out
    assert "- file2.txt" in captured.out

    assert result == [["file1.txt", "file2.txt"]]
    assert (tmp_path / "file1.txt").exists()
    assert not (tmp_path / "file2.txt").exists()
    assert (tmp_path / "file3.txt").exists()
