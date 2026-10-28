from pathlib import Path

from arcane.analysis import ClassifyResult, CopiedEntry, FailedEntry


def test_new_result_is_empty():
    result = ClassifyResult()

    assert result.copied == []
    assert result.skipped == []
    assert result.failed == []


def test_results_do_not_share_their_lists():
    first = ClassifyResult()
    second = ClassifyResult()

    first.copied.append(CopiedEntry(Path("a.txt"), Path("out/txt/a.txt")))
    first.skipped.append(Path("b.txt"))
    first.failed.append(FailedEntry(Path("c.txt"), "permission denied"))

    assert second.copied == []
    assert second.skipped == []
    assert second.failed == []


def test_entries_expose_named_fields():
    copied = CopiedEntry(Path("a.txt"), Path("out/a.txt"))
    failed = FailedEntry(Path("c.txt"), "missing")

    assert copied.source == Path("a.txt")
    assert copied.destination == Path("out/a.txt")
    assert failed.path == Path("c.txt")
    assert failed.reason == "missing"
