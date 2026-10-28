import os
from datetime import datetime, timezone

import pytest

from arcane.analysis import by_date


def make_file_at(directory, moment):
    """Create a file whose modification time is `moment` (a UTC datetime)."""
    path = directory / "dated.txt"
    path.write_bytes(b"x")
    timestamp = moment.timestamp()
    os.utime(path, (timestamp, timestamp))
    return path


@pytest.mark.parametrize(
    "moment, expected",
    [
        (datetime(2024, 3, 15, 12, 0, tzinfo=timezone.utc), "2024-03"),
        (datetime(2024, 1, 31, 23, 59, 59, tzinfo=timezone.utc), "2024-01"),
        (datetime(2024, 2, 1, 0, 0, 0, tzinfo=timezone.utc), "2024-02"),
        (datetime(2023, 12, 31, 23, 59, 59, tzinfo=timezone.utc), "2023-12"),
        (datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc), "2024-01"),
    ],
)
def test_by_date(tmp_path, moment, expected):
    assert by_date(make_file_at(tmp_path, moment)) == expected


def test_by_date_raises_on_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        by_date(tmp_path / "absent.txt")
