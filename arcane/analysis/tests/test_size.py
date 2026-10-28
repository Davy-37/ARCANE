import pytest

from arcane.analysis import by_size

KB = 1024
MB = 1024 * KB


def make_file(directory, size):
    """Create a file of exactly `size` bytes; truncate keeps big files cheap."""
    path = directory / f"file_{size}.bin"
    with path.open("wb") as handle:
        handle.truncate(size)
    return path


@pytest.mark.parametrize(
    "size, expected",
    [
        (0, "vide"),
        (1, "minuscule"),
        (10 * KB, "minuscule"),
        (10 * KB + 1, "petit"),
        (100 * KB, "petit"),
        (100 * KB + 1, "moyen"),
        (1 * MB, "moyen"),
        (1 * MB + 1, "grand"),
        (16 * MB, "grand"),
        (16 * MB + 1, "énorme"),
        (128 * MB, "énorme"),
        (128 * MB + 1, "gigantesque"),
    ],
)
def test_by_size(tmp_path, size, expected):
    assert by_size(make_file(tmp_path, size)) == expected


def test_by_size_raises_on_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        by_size(tmp_path / "absent.txt")
