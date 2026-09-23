from functools import lru_cache
import os
import random
import sys
import time


def random_coord(
    width: int,
    height: int,
) -> tuple[int, int]:
    return (random.randint(0, width), random.randint(0, height))


def valid_coord(coord: tuple[int, int], w: int, h: int) -> bool:
    return (0 <= coord[0] < w and 0 <= coord[1] < h)


def print_sleep(msg: str, delay: float = 1.05) -> None:
    print(msg)
    time.sleep(delay)


DEFAULT_COORD: tuple[int, int] = (0, 0)


DEFAULT_COORD_STR: str = "0,0"


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
