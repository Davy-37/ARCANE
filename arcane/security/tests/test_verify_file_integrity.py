import pytest

from arcane.security._sha256 import sha256
from arcane.security._verify_file_integrity import verify_file_integrity


def test_verify_identical_file(tmp_path):
    """Test that an unchanged file returns False."""
    file_path = tmp_path / "example.txt"
    file_path.write_text("Original content")

    original_hash = sha256(file_path)

    assert verify_file_integrity(file_path, original_hash) is False


def test_verify_modified_file(tmp_path):
    """Test that a modified file returns True."""
    file_path = tmp_path / "example.txt"
    file_path.write_text("Original content")

    original_hash = sha256(file_path)

    file_path.write_text("Modified content")

    assert verify_file_integrity(file_path, original_hash) is True


def test_verify_empty_file(tmp_path):
    """Test integrity verification of an empty file."""
    file_path = tmp_path / "empty.txt"
    file_path.write_bytes(b"")

    original_hash = sha256(file_path)

    assert verify_file_integrity(file_path, original_hash) is False


def test_verify_large_file(tmp_path):
    """Test integrity verification of a large file."""
    file_path = tmp_path / "large.bin"
    file_path.write_bytes(b"ARCANE" * 100_000)

    original_hash = sha256(file_path)

    assert verify_file_integrity(file_path, original_hash) is False


def test_verify_nonexistent_file(tmp_path):
    """Test that a nonexistent file raises FileNotFoundError."""
    file_path = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        verify_file_integrity(file_path, "dummy_hash")


def test_verify_directory(tmp_path):
    """Test that a directory raises IsADirectoryError."""
    with pytest.raises(IsADirectoryError):
        verify_file_integrity(tmp_path, "dummy_hash")
