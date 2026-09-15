# src/player/play_manager.py
from __future__ import annotations
from typing import TYPE_CHECKING

from mazegen import MazeGenerator

from player.constants import BOLD, RESET
from render.ascii.utils import hex_to_ansi_fg, move_cursor
from .keys import MenuKey, read_menu_key
from .menu import Menu, MenuItem

if TYPE_CHECKING:
    from render.base import MazeRenderer


class PlayManager:
    def __init__(self, generator: "MazeGenerator", render: "MazeRenderer") -> None:
        self.generator = generator,
        self.render = render
        self.game_over = False
        self.color: bool = False
        self.menu = Menu(items=[
            MenuItem("Show solution", lambda  : print("sooool")),
            MenuItem("Edit configuration", lambda  : print("sdooool")),
            MenuItem("Generate a new maze", self.generate_new_maze),
            MenuItem("Play", self.enter_play_mode),
            MenuItem("Exit", self.quit),
        ])

    def run(self) -> None:
        try:
            while not self.game_over:
                grid_height = len(self.render.display_grid)
                move_cursor(grid_height + 2, 1)
                self.render_menu()
                self._handle_input()
        except Exception as e:
            raise e


    def render_menu(self) -> None:
        self._menu_ansi() if self.color else self._menu_ascii()

    def _menu_options_text(self) -> list[str]:
        return ["1. Play", "2. Generate a new maze", "3. Exit"]

    def _menu_ascii(self) -> str:
        lines = ["+" + "-" * 40 + "+", "|{:^40}|".format("MENU"), "+" + "-" * 40 + "+"]
        lines += ["| {:<39}|".format(opt) for opt in self._menu_options_text()]
        lines.append("+" + "-" * 40 + "+")
        print("\n".join(lines))

    def _menu_ansi(self) -> str:
        accent = hex_to_ansi_fg(self.theme_color["special"])
        lines = [f"{accent}+{'-'*40}+{RESET}", f"{accent}|{RESET}{BOLD}{'MENU':^40}{accent}|{RESET}", f"{accent}+{'-'*40}+{RESET}"]
        lines += [f"{accent}| {RESET}{opt:<39}{accent}|{RESET}" for opt in self._menu_options_text()]
        lines.append(f"{accent}+{'-'*40}+{RESET}")
        print("\n".join(lines))

    def set_game_over(self, value: bool) -> None:
        self.game_over = value

    def quit(self) -> None:
        self.game_over = True

    def _handle_input(self) -> None:
        key = read_menu_key()
        if key is MenuKey.UP:
            self.menu.move_up()
        elif key is MenuKey.DOWN:
            self.menu.move_down()
        elif key is MenuKey.SELECT:
            self.menu.selected_item().action()
        # IGNORED / QUIT-without-confirmation / anything else -> no-op,
        # loop asks again. This is the actual "block other keys" behavior.

    # ---- actions ---------------------------------------------------


    def edit_configuration(self) -> None:
        self.generator.generate()          # same seed, new/edited params

    def generate_new_maze(self) -> None:
        self.generator.seed = (self.generator.seed or 0) + 1
        self.generator.generate()

    def enter_play_mode(self) -> None:
        self.render.play_mode = True
        self.run()