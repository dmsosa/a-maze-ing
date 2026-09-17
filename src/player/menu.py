# src/player/menu.py
from typing import Any, Callable

from render.ascii.constants import CELL_WIDTH
from render.ascii.utils import hex_to_ansi_fg


MENU_WIDTH = 30


class MenuItem:
    def __init__(self, key: str, label: str, action: Callable[..., Any]):
        self.key = key
        self.label = label
        self.action = action

class Menu:
    def __init__(self, name: str, items: list[MenuItem]):
        self.name = name
        self.items = items
        self.selected_index: int = 0
        self.items_len = len(items)


    def move_up(self) -> None:
        self.selected_index = (self.selected_index - 1) % len(self.items)

    def move_down(self) -> None:
        self.selected_index = (self.selected_index + 1) % len(self.items)

    def selected_item(self) -> MenuItem:
        return self.items[self.selected_index]

    def labels(self) -> list[str]:
        return [item.label for item in self.items]


def print_menu_ascii(menu: Menu, chars: list[str]):
    corner_ul = chars[0]
    corner_ur = chars[1]
    corner_bl = chars[2]
    corner_br = chars[3]
    hor_bar = chars[4]
    ver_bar = chars[5]
    top_row = f"{corner_ul}" + hor_bar * MENU_WIDTH + f"{corner_ur}"
    bot_row = f"{corner_bl}" + hor_bar * MENU_WIDTH + f"{corner_br}"
    empty_row = ver_bar + " " * CELL_WIDTH + ver_bar
    lines = [
        top_row,
        ver_bar + "{:^{w}}".format(menu.name, w=MENU_WIDTH) + ver_bar,
        empty_row
    ]
    for i in range(0, menu.items_len):
        item = menu.items[i]
        is_selected = " >>" if i == menu.selected_index else ""
        line = f"{is_selected} [{i + 1} / {item.key}]: {item.label}"
        lines.append(ver_bar + "{:<{w}}".format(line, w=MENU_WIDTH) + ver_bar)
    lines.append(empty_row)
    lines.append(bot_row)
    print("\n".join(lines))

def print_menu_ansi(menu: Menu, chars: list[str], theme_color: dict[str, str]):
    corner_ul = chars[0]
    corner_ur = chars[1]
    corner_bl = chars[2]
    corner_br = chars[3]
    hor_bar = chars[4]
    ver_bar = chars[5]
    accent = hex_to_ansi_fg(theme_color["blocked"])
    highlight = hex_to_ansi_fg(theme_color["current"])
    reset = "\033[0m"
    top_row = f"{accent}{corner_ul}" + hor_bar * MENU_WIDTH + f"{corner_ur}{reset}"
    bot_row = f"{accent}{corner_bl}" + hor_bar * MENU_WIDTH + f"{corner_br}{reset}"
    accent_bar = accent + ver_bar + reset
    empty_row = accent_bar + "   " * MENU_WIDTH + accent_bar
    lines = [
        top_row,
        accent_bar + "{:^{w}}".format(menu.name, w=MENU_WIDTH * 3) + accent_bar,
        empty_row
    ]
    for i in range(0, menu.items_len):
        item = menu.items[i]
        is_selected = " >>" if i == menu.selected_index else ""
        color = highlight if is_selected else ""
        reset_color = reset if is_selected else ""
        text = f"{is_selected} [{i + 1} / {item.key}]: {item.label}"
        line = accent_bar + color + "{:<{w}}".format(text, w=MENU_WIDTH * 3) + reset_color + accent_bar
        lines.append(line)
    lines.append(empty_row)
    lines.append(bot_row)
    print("\n".join(lines))
