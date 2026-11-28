"""Build regular expressions for keyword search."""

import re


def _build_pattern(keyword: str, ignore_case: bool, whole_word: bool) -> re.Pattern:
    if not keyword:
        raise ValueError("keyword must not be empty")
    flags = re.IGNORECASE if ignore_case else 0
    pattern = rf"\b{re.escape(keyword)}\b" if whole_word else re.escape(keyword)
    return re.compile(pattern, flags)
