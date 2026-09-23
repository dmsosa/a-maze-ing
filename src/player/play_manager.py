# src/player/play_manager.py
from enum import Enum, auto
import sys
from typing import cast
from mazegen import MazeGenerator
from player.constants import USERNAME_REGEXP
from player.utils import print_exit_play
from render.ascii.utils import clear_from_cursor, clear_screen, move_cursor
from .keys import get_key
from .menu import Menu, MenuItem,  print_menu_ansi, \
      print_menu_ascii, print_menu_lines_ansi, print_menu_lines_ascii
from config import MazeConfiguration
from render import MazeRenderer


class PlayOption(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    JUMP = auto()
    SOLUTION = auto()
    QUIT = auto()


class PlayDirection(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"


class PlayManager:
    """
    This class needs the following information:
    self.game_over to determine when the game is ended
    self.handle_input
    self.options: dict[str, set[str]],
    to handle the input and determine which option was pressed,
    play manager iterates over all of its options, and checks if pressed_key
    is included in any of the option_set. If it is not, then it ignores key
    and continues to the next iteration of the loop
    """
    def __init__(
            self,
            maze_config: "MazeConfiguration",
            generator: "MazeGenerator",
            render: "MazeRenderer"
            ) -> None:
        self.generator = generator
        self.render = render
        self.maze_config = maze_config
        self.game_over = False
        self.menu: Menu | None = None
        self.color: bool = render.color
        self.fly_mode: bool = False
        self.move_count: int = 0
        self.level: int = 1
        self.score: int = 0
        self.player_name: str = ""
        self.output_file: str = "players.txt"
        self.players: list[tuple[str, int]] = []

    def run(self) -> None:
        self.input_player_name()
        while not self.game_over:
            self.render.play_mode = True
            if not self.menu:
                self.menu = Menu(
                    name="A-Maze-Ing player options",
                    items=[
                        MenuItem(
                            "W",
                            "Move up",
                            {"W", "w", "\x1b[A"},
                            lambda: self.move_player("N")
                            ),
                        MenuItem(
                            "S",
                            "Move down",
                            {"S", "s", "\x1b[B"},
                            lambda: self.move_player("S")
                            ),
                        MenuItem(
                            "D",
                            "Move right",
                            {"D", "d", "\x1b[C"},
                            lambda: self.move_player("E")
                            ),
                        MenuItem(
                            "A",
                            "Move left",
                            {"A", "a", "\x1b[D"},
                            lambda: self.move_player("W")
                            ),
                        MenuItem(
                            "O",
                            "Show solution",
                            {"O", "o"},
                            lambda: self.show_solution()
                            ),
                        MenuItem(
                            "Enter",
                            "Jump",
                            {"\r", "\n", "J"},
                            lambda: self.enter_fly_mode()
                            ),
                        MenuItem(
                            "Q",
                            "Quit",
                            {"q", "Q", "\x1b", "\x03"},
                            lambda: self.quit()
                            )
                        ],
                )
            clear_screen(self.color)
            self.render.print_grid()
            print("\n")
            self.print_play_status()
            self.print_menu(self.menu)
            try:
                self._handle_input()
            except KeyError as e:
                print(
                    f"Invalid key detected for menu '{self.menu.name}':\n{e}",
                    file=sys.stderr
                    )
                continue
            except Exception as e:
                print(
                    f"Unexpected error for menu '{self.menu.name}':\n{e}",
                    file=sys.stderr
                    )
                continue
            self.check_game_over()

    def input_player_name(self) -> None:
        self._cursor_after_maze()
        clear_from_cursor()
        print(
            "... Insert your name, must be written in lowercase: ", flush=True
        )
        username = ""
        while not USERNAME_REGEXP.fullmatch(username) is not None:
            username = sys.stdin.readline().strip('\n')
        self.player_name = username

    def print_play_status(self) -> None:
        items = [
            f"Current level: {self.level}",
            f"{self.player_name}'s score: {self.score}",
            f"Jumper mode: {self.fly_mode}"
        ]
        if self.render.color:
            print_menu_lines_ansi(
                "Maze Configuration Edit",
                items,
                self.render.theme_char,
                self.render.theme_color,
                self.render.cell_size
                )
        else:
            print_menu_lines_ascii(
                "Maze Configuration Edit",
                items,
                self.render.theme_char,
                self.render.cell_size
                )

    def check_game_over(self) -> None:
        if self.render.player_pos == self.render.exit:
            self.level += 1
            if self.level > 10:
                self.score += 20
            elif self.level > 15:
                self.score += 30
            elif self.level > 20:
                self.score += 40
            elif self.level > 25:
                self.score += 50
            else:
                self.score += 5
            self.render.player_pos = self.render.entry
            self.generate_new_maze()

    def _cursor_after_maze(self) -> None:
        row = self.render.height * 2 + 1
        move_cursor(row + 3, 1)

    def print_menu(self, active_menu: Menu) -> None:
        theme = self.render.theme_char
        corner_br = theme["corner"][0b0110]
        corner_bl = theme["corner"][0b1010]
        corner_ur = theme["corner"][0b0011]
        corner_ul = theme["corner"][0b1001]
        wall_n = cast(str, theme["wall_n"])
        wall_w = cast(str, theme["wall_w"])
        chars = [
            corner_br,
            corner_bl,
            corner_ur,
            corner_ul,
            wall_n,
            wall_w,
        ]
        if self.color:
            print_menu_ansi(
                active_menu,
                chars,
                self.render.theme_color,
                False,
                self.render.cell_size
                )
        else:
            print_menu_ascii(
                active_menu,
                chars,
                False,
                self.render.cell_size
                )

    def clear_print(self) -> None:
        clear_screen(self.color)
        self.render.print_grid()

    def quit(self) -> None:
        self.game_over = True
        self.generator.export_maze()
        self.players.append((self.player_name, self.score))
        content = ""
        for p, s in self.players:
            content += f"{p}: {s}\n"
        with open(
            self.output_file,
            "a",
            encoding="utf-8",
            newline="\n",
        ) as file:
            file.write(content)
        if self.maze_config.pretty:
            print_exit_play()
        self.render.player_pos = (0, 0)
        self.render.play_mode = False
        self.game_over = True

    def _handle_input(self) -> None:
        key = get_key()
        menu = cast(Menu, self.menu)
        menu.get_item(key).action()

    # ---- actions ---------------------------------------------------
    def show_solution(self) -> None:
        self.render.show_solution = not self.render.show_solution

    def move_player(self, dir: str) -> None:
        """
        Huge: render knows where to print the player icon instead
        of empty space thanks to the _cell_state_mask, which is
        checked inside function print_display_grid, so, the goal
        of this function is to update the self.render.player_pos
        and update self.render._cell_state_mask.
        But there are conditions: the function is going to return and
        do not move the player if the direction I am trying to move to
        has a wall or is out of bounds. (which in any case, would have
        a wall), how to determine that?

        only the render has access to the hexadecimal representation
        of the maze. It can check walls by checking the current bit in
        digits[player_pos[1]][player_pos[0]].
        play manager does not want to check walls.
        Just ask the render to update itself, then re-print the maze
        and the playable menu.
        it checks
        if has_wall(digits[1][0], direction)

        """
        if not self.render.set_player_pos(dir):
            print(
                "Invalid player movement: from "
                f"{self.render.player_pos} to {dir}", file=sys.stderr
            )
        self.move_count += 1

    def enter_fly_mode(self) -> None:
        self.render.fly_mode = not self.fly_mode

    def generate_new_maze(self) -> None:
        self.generator.seed = (self.generator.seed or 0) + 1
        self.render.solution_set = set()
        self.generator.generate()
