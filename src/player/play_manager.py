# src/player/play_manager.py
from enum import Enum, auto
import sys
from typing import TYPE_CHECKING
from mazegen import MazeGenerator
from player.constants import BOLD, RESET
from player.utils import print_goodbye, print_line
from render.ascii.utils import clear_screen, hex_to_ansi_fg, move_cursor
from .keys import MenuKey, read_menu_key
from .menu import Menu, MenuItem, print_menu_ansi, print_menu_ascii
from config import MazeConfiguration
from render import MazeRenderer


class PlayState(Enum):
    MENU = auto()
    CONFIG_MENU = auto()
    EXIT = auto()


class PlayManager:
    def __init__(self, maze_config: "MazeConfiguration", generator: "MazeGenerator", render: "MazeRenderer") -> None:
        self.generator = generator
        self.render = render
        self.maze_config = maze_config
        self.state = PlayState.MENU
        self.game_over = False
        self.color: bool = False
        self.theme_color = render.theme_color
        self.menu = Menu(
            name="A-Maze-Ing Menu",
            items=[
            MenuItem("S", "Show solution", self.show_solution),
            MenuItem("E", "Edit configuration", lambda : print("Hello")),
            MenuItem("G", "Generate a new maze", self.generate_new_maze),
            MenuItem("P", "Play", self.enter_play_mode),
            MenuItem("Q", "Quit", self.quit),
        ])
        self.config_menu: Menu | None = None  # built lazily in open_edit_config
        self.config_menu = Menu(
            name="Edit A-Maze-Ing Configuration",
            items=[
            MenuItem("I", "Width", lambda : print("Hello")),
            MenuItem("H", "Height", lambda : print("Hello")),
            MenuItem("P", "Perfect", lambda : print("Hello")),
            MenuItem("A", "Algorithm", lambda : print("Hello")),
            MenuItem("N", "Entry", lambda : print("Hello")),
        ])
    
    def run(self) -> None:
        try:
            while not self.game_over:
                clear_screen(self.color)
                self.render.print_grid()
                self.print_menu()
                self._handle_input()
        except Exception as e:
            raise e

    def print_menu(self) -> None:
        chars = [
            self.render.theme_char["corner"][0b0110],
            self.render.theme_char["corner"][0b1100],
            self.render.theme_char["corner"][0b0011],
            self.render.theme_char["corner"][0b1001],
            self.render.theme_char["wall_n"],
            self.render.theme_char["wall_w"],

        ]
        if self.state == PlayState.MENU:
            active_menu = self.menu
        elif self.state == PlayState.CONFIG_MENU:
            active_menu = self.config_menu
        if self.color:
            print_menu_ansi(active_menu, chars, self.theme_color)
        else:
            print_menu_ascii(active_menu, chars)

    def quit(self) -> None:
        self.game_over = True
        self.generator.export_maze()
        if self.maze_config.pretty:
            print_goodbye()
        print_line(f"saving output file to {self.maze_config.output_file}\n")

    def _handle_input(self) -> None:
        key = read_menu_key()
        active_menu = self.menu \
            if self.state == PlayState.MENU \
            else self.config_menu
        if key is MenuKey.UP:
            active_menu.move_up()
        elif key is MenuKey.DOWN:
            active_menu.move_down()
        elif key is MenuKey.SELECT:
            active_menu.selected_item().action()
        elif key is MenuKey.EXIT:
            if self.state == PlayState.CONFIG_MENU:
                self.state = PlayState.MENU
            elif self.state == PlayState.MENU:
                self.generator.export_maze()
                if self.maze_config.pretty:
                    print_goodbye()
                print_line(f"saving output file to {self.maze_config.output_file}\n")
                sys.exit(0)
        # IGNORED / QUIT-without-confirmation / anything else -> no-op,
        # loop asks again. This is the actual "block other keys" behavior.

    # ---- actions ---------------------------------------------------

    def show_solution(self) -> None:
        self.render.show_solution = not self.render.show_solution
        clear_screen(self.color)
        self.render.print_grid()
        return

    def open_config_menu(self) -> None:
        self._display_edit_config_menu()
        key = read_menu_key()
        if key is MenuKey.UP:
            self.menu.move_up()
        elif key is MenuKey.DOWN:
            self.menu.move_down()
        elif key is MenuKey.SELECT:
            self.menu_config.selected_item().action()

    def generate_new_maze(self) -> None:
        self.generator.seed = (self.generator.seed or 0) + 1
        self.generator.generate()

    def enter_play_mode(self) -> None:
        self.render.play_mode = True
        self.run()
