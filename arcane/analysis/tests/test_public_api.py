import arcane.analysis

PUBLIC_NAMES = {
    "ClassifyResult",
    "CopiedEntry",
    "duplicates",
    "FailedEntry",
    "File_classify",
    "by_date",
    "by_extension",
    "by_size",
    "resolve_destination",
}


def test_all_lists_the_public_api():
    assert set(arcane.analysis.__all__) == PUBLIC_NAMES


def test_every_name_in_all_exists():
    for name in arcane.analysis.__all__:
        assert hasattr(arcane.analysis, name)


def test_star_import_exposes_the_public_api():
    namespace = {}

    exec("from arcane.analysis import *", namespace)

    assert PUBLIC_NAMES <= set(namespace)
