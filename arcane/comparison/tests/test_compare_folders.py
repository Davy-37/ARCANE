import pytest

from arcane.comparison import compare_folders


def test_compare_folders(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "deleted.txt").write_text("Hello")
    (tmp_path_new / "added.txt").write_text("Hello")

    (tmp_path_old / "modified.txt").write_text("Hello")
    (tmp_path_new / "modified.txt").write_text("World")

    (tmp_path_old / "unchanged.txt").write_text("Hello")
    (tmp_path_new / "unchanged.txt").write_text("Hello")

    result = compare_folders(tmp_path_old, tmp_path_new)

    assert result == {
        "added": ["added.txt"],
        "deleted": ["deleted.txt"],
        "modified": ["modified.txt"],
    }


def test_no_differences(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "file1.txt").write_text("Hello")
    (tmp_path_new / "file1.txt").write_text("Hello")

    result = compare_folders(tmp_path_old, tmp_path_new)

    assert result == {
        "added": [],
        "deleted": [],
        "modified": [],
    }


def test_empty_folders(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    result = compare_folders(tmp_path_old, tmp_path_new)

    assert result == {
        "added": [],
        "deleted": [],
        "modified": [],
    }


def test_added_only(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "deleted.txt").write_text("Hello")
    (tmp_path_new / "added.txt").write_text("Hello")

    (tmp_path_old / "modified.txt").write_text("Hello")
    (tmp_path_new / "modified.txt").write_text("World")

    result = compare_folders(
        tmp_path_old, tmp_path_new, added=True, deleted=False, modified=False
    )

    assert result == {"added": ["added.txt"]}


def test_deleted_only(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "deleted.txt").write_text("Hello")
    (tmp_path_new / "added.txt").write_text("Hello")

    (tmp_path_old / "modified.txt").write_text("Hello")
    (tmp_path_new / "modified.txt").write_text("World")

    result = compare_folders(
        tmp_path_old, tmp_path_new, added=False, deleted=True, modified=False
    )

    assert result == {"deleted": ["deleted.txt"]}


def test_modified_only(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "deleted.txt").write_text("Hello")
    (tmp_path_new / "added.txt").write_text("Hello")

    (tmp_path_old / "modified.txt").write_text("Hello")
    (tmp_path_new / "modified.txt").write_text("World")

    result = compare_folders(
        tmp_path_old, tmp_path_new, added=False, deleted=False, modified=True
    )

    assert result == {"modified": ["modified.txt"]}


def test_all_disabled(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "deleted.txt").write_text("Hello")
    (tmp_path_new / "added.txt").write_text("Hello")

    (tmp_path_old / "modified.txt").write_text("Hello")
    (tmp_path_new / "modified.txt").write_text("World")

    result = compare_folders(
        tmp_path_old, tmp_path_new, added=False, deleted=False, modified=False
    )

    assert result == {}


def test_display(tmp_path, capsys):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "deleted.txt").write_text("Hello")
    (tmp_path_new / "added.txt").write_text("Hello")

    (tmp_path_old / "modified.txt").write_text("Hello")
    (tmp_path_new / "modified.txt").write_text("World")

    result = compare_folders(tmp_path_old, tmp_path_new, display=True)

    assert result == {
        "added": ["added.txt"],
        "deleted": ["deleted.txt"],
        "modified": ["modified.txt"],
    }

    captured = capsys.readouterr()

    assert "+ added.txt" in captured.out
    assert "- deleted.txt" in captured.out
    assert "~ modified.txt" in captured.out


def test_no_display(tmp_path, capsys):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()
    tmp_path_new.mkdir()

    (tmp_path_old / "deleted.txt").write_text("Hello")
    (tmp_path_new / "added.txt").write_text("Hello")

    (tmp_path_old / "modified.txt").write_text("Hello")
    (tmp_path_new / "modified.txt").write_text("World")

    result = compare_folders(tmp_path_old, tmp_path_new)

    assert result == {
        "added": ["added.txt"],
        "deleted": ["deleted.txt"],
        "modified": ["modified.txt"],
    }

    captured = capsys.readouterr()

    assert captured.out == ""


def test_old_folder_not_found(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_new.mkdir()

    with pytest.raises(FileNotFoundError):
        compare_folders(tmp_path_old, tmp_path_new)


def test_new_folder_not_found(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.mkdir()

    with pytest.raises(FileNotFoundError):
        compare_folders(tmp_path_old, tmp_path_new)


def test_old_folder_not_a_directory(tmp_path):
    tmp_path_old = tmp_path / "old.txt"
    tmp_path_new = tmp_path / "new"

    tmp_path_old.write_text("Hello")
    tmp_path_new.mkdir()

    with pytest.raises(NotADirectoryError):
        compare_folders(tmp_path_old, tmp_path_new)


def test_new_folder_not_a_directory(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new.txt"

    tmp_path_old.mkdir()
    tmp_path_new.write_text("Hello")

    with pytest.raises(NotADirectoryError):
        compare_folders(tmp_path_old, tmp_path_new)


def test_invalid_folder_all_disabled(tmp_path):
    tmp_path_old = tmp_path / "old"
    tmp_path_new = tmp_path / "new"

    tmp_path_new.mkdir()

    with pytest.raises(FileNotFoundError):
        compare_folders(
            tmp_path_old,
            tmp_path_new,
            added=False,
            deleted=False,
            modified=False,
        )
