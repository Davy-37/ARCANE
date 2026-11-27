import pytest

from arcane.search import (
    contains_word,
    count_occurrences,
    find_lines,
    get_context,
    search_in_folder,
)


@pytest.mark.parametrize(
    ("content", "keyword", "options", "expected"),
    [
        ("A quick FOX", "fox", {}, True),
        ("A quick FOX", "fox", {"ignore_case": False}, False),
        ("the foxes", "fox", {"whole_word": True}, False),
        ("the fox!", "fox", {"whole_word": True}, True),
        ("a.b", "a.b", {}, True),
        ("axb", "a.b", {}, False),
        ("", "fox", {}, False),
    ],
)
def test_contains_word_options(tmp_path, content, keyword, options, expected):
    path = tmp_path / "sample.txt"
    path.write_text(content, encoding="utf-8")

    assert contains_word(str(path), keyword, **options) is expected


def test_find_lines_returns_matching_line_numbers_and_contents(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text("First fox\nno match\nFOX again\n", encoding="utf-8")

    assert find_lines(path, "fox") == [(1, "First fox"), (3, "FOX again")]
    assert find_lines(path, "fox", ignore_case=False) == [(1, "First fox")]
    assert find_lines(path, "missing") == []


def test_count_occurrences_counts_repeated_matches(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text("cat CAT caterpillar\n", encoding="utf-8")

    assert count_occurrences(path, "cat") == 3
    assert count_occurrences(path, "cat", whole_word=True) == 2
    assert count_occurrences(path, "cat", ignore_case=False) == 2
    assert count_occurrences(path, "missing") == 0


def test_get_context_returns_lines_before_and_after_match(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text("one\ntwo\nneedle\nfour\nfive\n", encoding="utf-8")

    assert get_context(path, "needle", lines_around=1) == [
        {"line_num": 3, "context": ["two", "needle", "four"]}
    ]


def test_get_context_returns_partial_context_at_end_of_file(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text("one\nneedle\nthree\n", encoding="utf-8")

    assert get_context(path, "needle", lines_around=2) == [
        {"line_num": 2, "context": ["one", "needle", "three"]}
    ]


def test_get_context_handles_overlapping_matches(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text("needle 1\nneedle 2\nend\nneedle 3\n", encoding="utf-8")

    assert get_context(path, "needle", lines_around=1) == [
        {"line_num": 1, "context": ["needle 1", "needle 2"]},
        {"line_num": 2, "context": ["needle 1", "needle 2", "end"]},
        {"line_num": 4, "context": ["end", "needle 3"]},
    ]


def test_get_context_with_zero_lines_and_no_match(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text("needle\nNEEDLE\nother\n", encoding="utf-8")

    assert get_context(path, "needle", lines_around=0) == [
        {"line_num": 1, "context": ["needle"]},
        {"line_num": 2, "context": ["NEEDLE"]},
    ]
    assert get_context(path, "missing") == []
    with pytest.raises(ValueError):
        get_context(path, "needle", lines_around=-1)


def test_search_in_folder_filters_extensions_and_searches_recursively(tmp_path):
    nested = tmp_path / "nested"
    nested.mkdir()
    matching = nested / "match.txt"
    csv = tmp_path / "other.csv"
    no_extension = tmp_path / "README"
    (tmp_path / "empty.txt").touch()
    matching.write_text("find this needle", encoding="utf-8")
    csv.write_text("find this NEEDLE", encoding="utf-8")
    no_extension.write_text("needles", encoding="utf-8")

    assert search_in_folder(tmp_path, "needle", extensions="txt") == [matching]
    assert set(search_in_folder(tmp_path, "needle", extensions=[".txt", "csv"])) == {
        matching,
        csv,
    }
    assert set(search_in_folder(tmp_path, "needle", recursive=False)) == {
        csv,
        no_extension,
    }
    assert set(search_in_folder(tmp_path, "needle")) == {matching, csv, no_extension}
    assert set(search_in_folder(tmp_path, "needle", extensions=[])) == {
        matching,
        csv,
        no_extension,
    }
    assert set(search_in_folder(tmp_path, "needle", whole_word=True)) == {
        matching,
        csv,
    }
    assert set(search_in_folder(tmp_path, "needle", ignore_case=False)) == {
        matching,
        no_extension,
    }
    assert search_in_folder(tmp_path, "missing") == []
    assert search_in_folder(tmp_path / "missing", "needle") == []
    assert search_in_folder(matching, "needle") == []


@pytest.mark.parametrize(
    "search_function", [contains_word, find_lines, count_occurrences, get_context]
)
def test_file_search_rejects_empty_keyword_and_missing_file(tmp_path, search_function):
    path = tmp_path / "sample.txt"
    path.touch()

    with pytest.raises(ValueError):
        search_function(path, "")
    with pytest.raises(FileNotFoundError):
        search_function(tmp_path / "missing.txt", "needle")


def test_folder_search_rejects_empty_keyword(tmp_path):
    with pytest.raises(ValueError):
        search_in_folder(tmp_path, "")
