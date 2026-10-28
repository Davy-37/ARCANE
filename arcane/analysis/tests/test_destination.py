from arcane.analysis import resolve_destination


def write(path, content=b"x"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


def test_resolve_destination_without_collision(tmp_path):
    source = write(tmp_path / "src" / "rapport.pdf")
    out = tmp_path / "out"
    out.mkdir()

    assert resolve_destination(source, out) == out / "rapport.pdf"


def test_resolve_destination_renames_when_content_differs(tmp_path):
    source = write(tmp_path / "src" / "rapport.pdf", b"new")
    out = tmp_path / "out"
    write(out / "rapport.pdf", b"old")

    assert resolve_destination(source, out) == out / "rapport_1.pdf"


def test_resolve_destination_increments_suffix(tmp_path):
    source = write(tmp_path / "src" / "rapport.pdf", b"new")
    out = tmp_path / "out"
    write(out / "rapport.pdf", b"old")
    write(out / "rapport_1.pdf", b"older")

    assert resolve_destination(source, out) == out / "rapport_2.pdf"


def test_resolve_destination_returns_none_when_identical(tmp_path):
    source = write(tmp_path / "src" / "rapport.pdf", b"same")
    out = tmp_path / "out"
    write(out / "rapport.pdf", b"same")

    assert resolve_destination(source, out) is None


def test_resolve_destination_returns_none_when_identical_to_renamed_copy(tmp_path):
    source = write(tmp_path / "src" / "rapport.pdf", b"new")
    out = tmp_path / "out"
    write(out / "rapport.pdf", b"old")
    write(out / "rapport_1.pdf", b"new")

    assert resolve_destination(source, out) is None


def test_resolve_destination_without_extension(tmp_path):
    source = write(tmp_path / "src" / "README", b"new")
    out = tmp_path / "out"
    write(out / "README", b"old")

    assert resolve_destination(source, out) == out / "README_1"
