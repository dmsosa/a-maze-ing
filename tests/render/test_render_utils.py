# test_render.py
import pytest
from typing import Any
from render.utils import (
    move_cursor,
    save_cursor,
    restore_cursor,
    print_square,
)


# ── Move Cursor ───────────────────────────────────────────────────────

def test_move_cursor_origin(capsys: Any) -> None:
    move_cursor(0, 0)
    assert capsys.readouterr().out == "\033[0;0H"


def test_move_cursor_position(capsys: Any) -> None:
    move_cursor(10, 20)
    assert capsys.readouterr().out == "\033[10;20H"


def test_move_cursor_large_values(capsys: Any) -> None:
    move_cursor(50, 120)
    assert capsys.readouterr().out == "\033[50;120H"


# ── Save Cursor ───────────────────────────────────────────────────────

def test_save_cursor(capsys: Any) -> None:
    save_cursor()
    assert capsys.readouterr().out == "\033[s"


# ── Restore Cursor ────────────────────────────────────────────────────

def test_restore_cursor(capsys: Any) -> None:
    restore_cursor()
    assert capsys.readouterr().out == "\033[u"


# ── Print Square ──────────────────────────────────────────────────────

def test_print_square_hex_red(capsys: Any) -> None:
    print_square("#FF0000")
    out = capsys.readouterr().out
    assert "\033[48;2;255;0;0m" in out
    assert "█" in out
    assert "\033[0m" in out


def test_print_square_hex_blue(capsys: Any) -> None:
    print_square("#0000FF")
    out = capsys.readouterr().out
    assert "\033[48;2;0;0;255m" in out


def test_print_square_hex_white(capsys: Any) -> None:
    print_square("#FFFFFF")
    out = capsys.readouterr().out
    assert "\033[48;2;255;255;255m" in out


def test_print_square_hex_black(capsys: Any) -> None:
    print_square("#000000")
    out = capsys.readouterr().out
    assert "\033[48;2;0;0;0m" in out


def test_print_square_resets_after(capsys: Any) -> None:
    print_square("#123456")
    out = capsys.readouterr().out
    assert out.endswith("\033[0m")


def test_print_square_valid_hex_length() -> None:
    with pytest.raises(ValueError):
        print_square("#FFF")  # too short


def test_print_square_invalid_hex_chars() -> None:
    with pytest.raises(ValueError):
        print_square("#GGGGGG")


# ── Integration: save → move → restore ────────────────────────────────

def test_cursor_save_restore_sequence(capsys: Any) -> None:
    save_cursor()
    move_cursor(5, 5)
    restore_cursor()
    out = capsys.readouterr().out
    assert out == "\033[s\033[5;5H\033[u"
