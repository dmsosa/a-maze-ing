# src/player/keys.py
from enum import Enum, auto
import time
import sys, tty, termios


class MenuKey(Enum):
    UP = auto()
    DOWN = auto()
    SELECT = auto()
    EXIT = auto()
    IGNORED = auto()


class PlayMenuKey(Enum):
    EDIT_CONFIG = "edit_config"
    NEW_MAZE = "new_maze"
    PLAY = "play"
    PERFECT = "perfect"


class ConfigMenuKey(Enum):
    WIDTH = "width"
    HEIGHT = "height"
    PERFECT = "perfect"
    ALGORITHM = "algorithm"


_ARROW_UP = {"\x1b[A", "W", "w"}     # POSIX escape seq / Windows scan code
_ARROW_DOWN = {"\x1b[B", "S", "s"}
_ENTER = {"\r", "\n"}
_EXIT = {"q", "Q", "\x1b", "\x03"} # bare ESC and Ctrl+C

MENU_KEYS = {
    "width": {"1", "I", "i"},
    "height": {"2", "H", "h"},
    "perfect": {"3", "P", "p"},
    "algorithm": {"4", "A", "a"}
}


CONFIG_MENU_KEYS = {
    "width": {"1", "I", "i"},
    "height": {"2", "H", "h"},
    "perfect": {"3", "P", "p"},
    "algorithm": {"4", "A", "a"}
}

def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        seq = _read_logical_key()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return seq


def _read_logical_key(delay: float = 0.05) -> str:
    """
    Collapse a multi-byte arrow-key sequence into one token.
    After reading ESC, try to read the rest of an escape sequence
    """
    first = sys.stdin.read(1)

    if first == "\x1b":
        my_timeout = time.monotonic() + delay
        while time.monotonic() < my_timeout:
            second = sys.stdin.read(1)
            if second == "[":
                third = sys.stdin.read(1)
                return first + second + third
            else:
                return first
    return first


def read_menu_key() -> MenuKey:
    raw = get_key()
    if raw in _ARROW_UP:
        return MenuKey.UP
    if raw in _ARROW_DOWN:
        return MenuKey.DOWN
    if raw in _ENTER:
        return MenuKey.SELECT
    if raw in _EXIT:
        return MenuKey.EXIT
    return MenuKey.IGNORED


def read_config_menu_key() -> MenuKey:
    raw = get_key()
    if raw in _ARROW_UP:
        return MenuKey.UP
    if raw in _ARROW_DOWN:
        return MenuKey.DOWN
    if raw in _ENTER:
        return MenuKey.SELECT
    if raw in _EXIT:
        return MenuKey.EXIT
    if raw in CONFIG_MENU_KEYS["width"]:
        return ConfigMenuKey.WIDTH
    if raw in CONFIG_MENU_KEYS["height"]:
        return ConfigMenuKey.HEIGHT
    if raw in CONFIG_MENU_KEYS["perfect"]:
        return ConfigMenuKey.PERFECT
    if raw in CONFIG_MENU_KEYS["algorithm"]:
        return ConfigMenuKey.ALGORITHM
    return MenuKey.IGNORED
