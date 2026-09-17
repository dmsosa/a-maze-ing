import random
import time


def random_coord(
    width: int,
    height: int,
) -> tuple[int, int]:
    return (random.randint(0, width), random.randint(0, height))


def valid_coord(coord: tuple[int, int], w: int, h: int):
    return (0 <= coord[0] < w and 0 <= coord[1] < h)


def print_sleep(msg: str, delay = 1.05):
        print(msg)
        time.sleep(delay)


DEFAULT_COORD: tuple[int, int] = (0,0)
DEFAULT_COORD_STR: str = "0,0"
