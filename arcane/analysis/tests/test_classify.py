import os
from datetime import datetime, timezone

import pytest

from arcane.analysis import CopiedEntry, File_classify


def write(path, content=b"x"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


def test_classify_copies_by_extension_and_keeps_originals(tmp_path):
    pdf = write(tmp_path / "src" / "rapport.pdf", b"pdf")
    jpg = write(tmp_path / "src" / "PHOTO.JPG", b"jpg")
    out = tmp_path / "out"

    result = File_classify([pdf, jpg], "extension", out)

    assert (out / "pdf" / "rapport.pdf").read_bytes() == b"pdf"
    assert (out / "jpg" / "PHOTO.JPG").read_bytes() == b"jpg"
    assert pdf.exists() and jpg.exists()
    assert result.copied == [
        CopiedEntry(pdf, out / "pdf" / "rapport.pdf"),
        CopiedEntry(jpg, out / "jpg" / "PHOTO.JPG"),
    ]
    assert result.skipped == []
    assert result.failed == []


def test_classify_preserves_metadata(tmp_path):
    source = write(tmp_path / "src" / "a.txt")
    os.utime(source, (1_000_000_000, 1_000_000_000))
    out = tmp_path / "out"

    File_classify([source], "extension", out)

    assert (out / "txt" / "a.txt").stat().st_mtime == 1_000_000_000


def test_classify_skips_identical_files_on_second_run(tmp_path):
    source = write(tmp_path / "src" / "a.txt", b"same")
    out = tmp_path / "out"
    File_classify([source], "extension", out)

    result = File_classify([source], "extension", out)

    assert result.copied == []
    assert result.skipped == [source]
    assert sorted(p.name for p in (out / "txt").iterdir()) == ["a.txt"]


def test_classify_renames_on_collision(tmp_path):
    first = write(tmp_path / "one" / "rapport.pdf", b"first")
    second = write(tmp_path / "two" / "rapport.pdf", b"second")
    out = tmp_path / "out"

    result = File_classify([first, second], "extension", out)

    assert (out / "pdf" / "rapport.pdf").read_bytes() == b"first"
    assert (out / "pdf" / "rapport_1.pdf").read_bytes() == b"second"
    assert result.copied[1].destination == out / "pdf" / "rapport_1.pdf"


def test_classify_reuses_existing_destination(tmp_path):
    source = write(tmp_path / "src" / "a.txt")
    out = tmp_path / "out"
    (out / "txt").mkdir(parents=True)

    result = File_classify([source], "extension", out)

    assert len(result.copied) == 1


def test_classify_by_size_and_date(tmp_path):
    source = write(tmp_path / "src" / "a.txt")
    moment = datetime(2024, 3, 15, tzinfo=timezone.utc).timestamp()
    os.utime(source, (moment, moment))

    File_classify([source], "size", tmp_path / "by_size")
    File_classify([source], "date", tmp_path / "by_date")

    assert (tmp_path / "by_size" / "minuscule" / "a.txt").exists()
    assert (tmp_path / "by_date" / "2024-03" / "a.txt").exists()


def test_classify_unknown_criterion_raises_before_any_action(tmp_path):
    source = write(tmp_path / "src" / "a.txt")
    out = tmp_path / "out"

    with pytest.raises(ValueError):
        File_classify([source], "color", out)

    assert not out.exists()


def test_classify_collects_failures_and_continues(tmp_path):
    missing = tmp_path / "src" / "absent.txt"
    good = write(tmp_path / "src" / "good.txt")
    out = tmp_path / "out"

    result = File_classify([missing, good], "size", out)

    assert [entry.path for entry in result.failed] == [missing]
    assert result.failed[0].reason
    assert [entry.source for entry in result.copied] == [good]


def test_classify_default_destination_is_in_current_directory(tmp_path, monkeypatch):
    source = write(tmp_path / "src" / "a.txt")
    monkeypatch.chdir(tmp_path)

    File_classify([source], "extension")

    assert (tmp_path / "classified" / "txt" / "a.txt").exists()
