# src/player/keys.py
from enum import Enum, auto
import time
import sys
import tty
import termios

from mazegen import MazeAlgorithm
from mazegen.model.constants import SolutionAlgorithm
from render.ascii.constants import RENDER_THEMES_CHARS, RENDER_THEMES_COLORS
from render.ascii.utils import move_cursor_up


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
_EXIT = {"q", "Q", "\x1b", "\x03"}  # bare ESC and Ctrl+C


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
    return raw


def read_boolean_key() -> bool:
    idx = 0
    while True:
        print("\r", flush=True)
        bools = [True, False]
        for i in range(0, len(bools)):
            label = "True" if bools[i] else "False"
            selected = " >> " if idx % 2 == i else "    "
            print(f"{selected} {label}", end="")
            if i < 2:
                print("")
        key = read_menu_key()
        if key is MenuKey.UP:
            idx = (idx - 1) % 2
        if key is MenuKey.DOWN:
            idx = (idx + 1) % 2
        if key is MenuKey.SELECT:
            new_value = bools[idx]
            return new_value
        if key is MenuKey.EXIT:
            break
        move_cursor_up(3)


def read_algorithm_key() -> MazeAlgorithm:
    values = list(MazeAlgorithm)
    values_len = len(values)
    idx = 0
    while True:
        print("\r", flush=True)
        for i, algo in enumerate(values):
            selected = " >> " if idx % values_len == i else ""
            print(f"{selected}[{i + 0}]: {algo.name}")
        key = read_menu_key()
        if key is MenuKey.UP:
            idx = (idx - 1) % values_len
        if key is MenuKey.DOWN:
            idx = (idx + 1) % values_len
        if key is MenuKey.SELECT:
            new_value = values[idx]
            return new_value
        if key is MenuKey.EXIT:
            break
        move_cursor_up(values_len + 1)


def read_sol_algorithm_key() -> SolutionAlgorithm:
    values = list(SolutionAlgorithm)
    values_len = len(values)
    idx = 0
    while True:
        print("\r", flush=True)
        for i, algo in enumerate(values):
            selected = " >> " if idx % values_len == i else ""
            print(f"{selected}[{i + 0}]: {algo.name}")
        key = read_menu_key()
        if key is MenuKey.UP:
            idx = (idx - 1) % values_len
        if key is MenuKey.DOWN:
            idx = (idx + 1) % values_len
        if key is MenuKey.SELECT:
            new_value = values[idx]
            return new_value
        if key is MenuKey.EXIT:
            break
        move_cursor_up(values_len + 1)


def read_theme_char_key() -> str:
    values = list(RENDER_THEMES_CHARS.keys())
    values_len = len(values)
    idx = 0
    while True:
        print("\r", flush=True)
        for i, value in enumerate(values):
            selected = " >> " if idx % values_len == i else ""
            print(f"{selected}[{i + 0}]: {value}")
        key = read_menu_key()
        if key is MenuKey.UP:
            idx = (idx - 1) % values_len
        if key is MenuKey.DOWN:
            idx = (idx + 1) % values_len
        if key is MenuKey.SELECT:
            new_value = values[idx]
            return new_value
        if key is MenuKey.EXIT:
            break
        move_cursor_up(values_len + 1)


def read_theme_color_key() -> str:
    values = list(RENDER_THEMES_COLORS.keys())
    values_len = len(values)
    idx = 0
    while True:
        print("\r", flush=True)
        for i, value in enumerate(values):
            selected = " >> " if idx % values_len == i else ""
            print(f"{selected}[{i + 0}]: {value}")
        key = read_menu_key()
        if key is MenuKey.UP:
            idx = (idx - 1) % values_len
        if key is MenuKey.DOWN:
            idx = (idx + 1) % values_len
        if key is MenuKey.SELECT:
            new_value = values[idx]
            return new_value
        if key is MenuKey.EXIT:
            break
        move_cursor_up(values_len + 1)
