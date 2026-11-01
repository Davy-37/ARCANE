import hashlib

import pytest

from arcane.security._sha256 import sha256


def test_sha256_known_content(tmp_path):
    """Test SHA-256 hashing with known file content."""
    file_path = tmp_path / "example.txt"
    file_path.write_bytes(b"hello world")

    expected = hashlib.sha256(b"hello world").hexdigest()

    assert sha256(file_path) == expected


def test_sha256_empty_file(tmp_path):
    """Test SHA-256 hashing of an empty file."""
    file_path = tmp_path / "empty.txt"
    file_path.write_bytes(b"")

    expected = hashlib.sha256(b"").hexdigest()

    assert sha256(file_path) == expected


def test_sha256_modified_file(tmp_path):
    """Test that modifying a file changes its SHA-256 hash."""
    file_path = tmp_path / "example.txt"
    file_path.write_text("Original content")

    original_hash = sha256(file_path)

    file_path.write_text("Modified content")

    assert sha256(file_path) != original_hash


def test_sha256_large_file(tmp_path):
    """Test SHA-256 hashing of a file larger than the read buffer."""
    file_path = tmp_path / "large.bin"
    content = b"ARCANE" * 100_000
    file_path.write_bytes(content)

    expected = hashlib.sha256(content).hexdigest()

    assert sha256(file_path) == expected


def test_sha256_nonexistent_file(tmp_path):
    """Test that a missing file raises FileNotFoundError."""
    file_path = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        sha256(file_path)


def test_sha256_directory(tmp_path):
    """Test that a directory cannot be hashed as a regular file."""
    with pytest.raises(IsADirectoryError):
        sha256(tmp_path)
