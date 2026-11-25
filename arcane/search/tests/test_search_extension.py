from arcane.search import (
    by_extension,
)


def test_by_extension_accepts_string_or_list_and_normalizes_dot(tmp_path):
    text_file = tmp_path / "notes.txt"
    csv_file = tmp_path / "data.csv"
    (tmp_path / "image.png").touch()
    text_file.touch()
    csv_file.touch()

    assert set(by_extension(tmp_path, "txt")) == {text_file}
    assert set(by_extension(tmp_path, [".txt", "csv"])) == {
        text_file,
        csv_file,
    }


def test_by_extension_respects_recursive_option(tmp_path):
    direct_file = tmp_path / "direct.txt"
    nested_dir = tmp_path / "nested"
    nested_dir.mkdir()
    nested_file = nested_dir / "nested.txt"
    direct_file.touch()
    nested_file.touch()

    assert set(by_extension(tmp_path, ".txt", recursive=False)) == {direct_file}
    assert set(by_extension(tmp_path, ".txt")) == {direct_file, nested_file}


def test_by_extension_returns_empty_for_missing_directory(tmp_path):
    assert by_extension(tmp_path / "missing", ".txt") == []
