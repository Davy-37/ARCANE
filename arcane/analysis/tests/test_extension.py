from pathlib import Path

import pytest

from arcane.analysis import by_extension


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("rapport.pdf", "pdf"),
        ("PHOTO.JPG", "jpg"),
        ("Notes.TxT", "txt"),
        ("README", "sans_extension"),
        (".gitignore", "sans_extension"),
        ("archive.tar.gz", "gz"),
    ],
)
def test_by_extension(filename, expected):
    assert by_extension(Path(filename)) == expected


def test_by_extension_does_not_need_the_file_to_exist(tmp_path):
    assert by_extension(tmp_path / "absent.csv") == "csv"
