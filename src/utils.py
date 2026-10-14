from functools import lru_cache
import os
import sys


@lru_cache
def supports_ansi() -> bool:
    """
    Best-effort check for whether stdout will interpret ANSI escape codes.
    """
    if os.environ.get("NO_COLOR") is not None:
        return False

    if not sys.stdout.isatty():
        return False

    term = os.environ.get("TERM", "")
    if term in ("dumb", ""):
        return False

    return True