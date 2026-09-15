# src/player/keys.py
from enum import Enum, auto
import sys, tty, termios


class MenuKey(Enum):
    UP = auto()
    DOWN = auto()
    SELECT = auto()
    QUIT = auto()
    IGNORED = auto()


_ARROW_UP = {"\x1b[A", "W"}     # POSIX escape seq / Windows scan code
_ARROW_DOWN = {"\x1b[B", "S"}
_ENTER = {"\r", "\n"}
_QUIT = {"q", "Q"}




def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch


def _read_logical_key() -> str:
    """Collapse a multi-byte arrow-key sequence into one token."""
    first = get_key()

    if first == "\x1b" and sys.platform != "win32":
        return first + get_key() + get_key()   # ESC [ A/B/C/D

    if first == "\xe0" and sys.platform == "win32":
        return get_key()                          # msvcrt special-key byte

    return first


def read_menu_key() -> MenuKey:
    raw = _read_logical_key()
    if raw in _ARROW_UP:
        return MenuKey.UP
    if raw in _ARROW_DOWN:
        return MenuKey.DOWN
    if raw in _ENTER:
        return MenuKey.SELECT
    if raw in _QUIT:
        return MenuKey.QUIT
    return MenuKey.IGNORED
