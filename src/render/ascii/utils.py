import os
import platform
import sys
import time

from constants import BOLD, \
    GREEN, \
    MAIN_INSTRUCTION, \
    RESET, \
    SUBTITLE, \
    TITLE, \
    YELLOW


def clear_screen(is_ansi: bool) -> None:
    """Call this ONCE, before the animation loop starts."""
    if is_ansi:
        sys.stdout.write("\033[2J\033[H")
    else:
        os.system("cls" if platform.system() == "Windows" else "clear")
    sys.stdout.flush()


def clear_from_cursor() -> None:
    sys.stdout.write("\x1b[J")


def print_char(char: str) -> None:
    sys.stdout.write(char)


def cursor_home() -> None:
    sys.stdout.write("\033[H")


def hide_cursor() -> None:
    sys.stdout.write("\033[?25l")


def show_cursor() -> None:
    sys.stdout.write("\033[?25h")


def move_cursor(row: int, col: int) -> None:
    sys.stdout.write(f"\033[{row};{col}H")


def move_cursor_right(columns: int) -> None:
    sys.stdout.write(f"\033[{columns}C")


def move_cursor_up(rows: int) -> None:
    sys.stdout.write(f"\033[{rows}A")


def save_cursor() -> None:
    sys.stdout.write("\033[s")


def restore_cursor() -> None:
    sys.stdout.write("\033[u")


def hex_to_ansi_fg(hex_color: str) -> str:
    """Convert '#rrggbb' to a 24-bit truecolor ANSI foreground escape."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"\033[38;2;{r};{g};{b}m"


def hex_to_ansi_bg(hex_color: str) -> str:
    """Convert '#rrggbb' to a 24-bit truecolor ANSI background escape."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"\033[48;2;{r};{g};{b}m"


HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


def print_line(s: str, delay: float = 0.05) -> None:
    for ch in s:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)


def erase_line(s: str) -> None:
    sys.stdout.write("\r" + " " * len(s) + "\r")
    sys.stdout.flush()


def print_presentation() -> None:
    print_line(f"{YELLOW}{MAIN_INSTRUCTION}{RESET}")
    erase_line(MAIN_INSTRUCTION)
    print_line(f"{BOLD}{GREEN}{TITLE}{RESET}")
    print_line(f"{BOLD}{GREEN}{SUBTITLE}{RESET}")
