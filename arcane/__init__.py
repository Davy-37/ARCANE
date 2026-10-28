"""arcane: a library to analyze, compare, search, and secure files and folders."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("arcane")
except PackageNotFoundError:  # pragma: no cover - source tree that is not installed
    __version__ = "unknown"

__all__: list[str] = []
