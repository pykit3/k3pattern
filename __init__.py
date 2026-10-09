"""
Find common prefix of several string, tuples of string, or other nested structure, recursively by default.
It returns the shortest prefix: empty string or empty tuple is removed.
"""

from .strutil import (
    common_prefix,
)

__all__ = [
    "common_prefix",
]


def __getattr__(name: str) -> str:
    # importlib.metadata takes about 20 ms to import, so it is loaded only
    # when __version__ is read
    if name != "__version__":
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    from importlib.metadata import version

    return version("k3pattern")
