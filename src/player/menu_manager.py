# src/player/menu_manager.py
from enum import Enum, auto
import sys

from mazegen import MazeGenerator
from pydantic import ValidationError

from config import MazeConfiguration
from player.utils import print_goodbye, print_line, str_to_coords
from render import MazeRenderer
from render.ascii import get_theme_chars, get_theme_colors
from render.ascii.utils import clear_from_cursor, clear_screen, move_cursor
from .keys import (
    MenuKey,
    read_algorithm_key,
    read_boolean_key,
    read_menu_key,
    read_sol_algorithm_key,
    read_theme_char_key,
    read_theme_color_key,
)
from .menu import (
    Menu,
    MenuItem,
    print_menu_ansi,
    print_menu_ascii,
    print_menu_lines_ansi,
    print_menu_lines_ascii,
)
from .play_manager import PlayManager


class MenuState(Enum):
    MENU = auto()
    CONFIG_MENU = auto()
    PLAY = auto()
    EXIT = auto()


class MenuManager:
    def __init__(
        self,
        maze_config: "MazeConfiguration",
        generator: "MazeGenerator",
        render: "MazeRenderer",
    ) -> None:
        self.generator = generator
        self.render = render
        self.maze_config = maze_config
        self.state = MenuState.MENU
        self.game_over = False
        self.color: bool = False
        self.menu: Menu | None = None
        self.config_menu: Menu | None = None  # built lazily
        self.play_manager: PlayManager | None = None  # built lazily

    def run(self) -> None:
        while self.state is not MenuState.EXIT:
            if not self.menu:
                self.menu = Menu(
                    name="Interactive A-Maze-Ing Menu",
                    items=[
                        MenuItem(
                            "O",
                            "Show/Hide solution",
                            {"O", "o"},
                            self.show_solution,
                        ),
                        MenuItem(
                            "E",
                            "Edit maze configuration",
                            {"E", "e"},
                            self.open_config_menu,
                        ),
                        MenuItem(
                            "G",
                            "Generate new maze",
                            {"G", "g"},
                            self.generate_new_maze,
                        ),
                        MenuItem(
                            "P",
                            "Enter into play mode",
                            {"P", "p"},
                            self.enter_play_mode,
                        ),
                        MenuItem(
                            "Q",
                            "Quit",
                            {"Q", "q"},
                            self.quit,
                        ),
                    ],
                )
            clear_screen(self.color)
            self.render.print_grid()
            if self.state == MenuState.MENU:
                active_menu = self.menu
            elif self.state == MenuState.CONFIG_MENU:
                active_menu = self.config_menu
            else:
                active_menu = self.menu
            self.print_menu(active_menu)
            try:
                self._handle_input(active_menu)
            except KeyError as exc:
                message = (
                    "Invalid key detected for menu "
                    f"'{active_menu.name}':\n{exc}"
                )
                print(message, file=sys.stderr)
                continue
            except Exception as exc:
                message = (
                    "Unexpected error raised for menu "
                    f"'{self.menu.name}':\n{exc}"
                )
                print(message, file=sys.stderr)
                continue

    def _cursor_after_maze(self) -> None:
        row = self.maze_config.height * 2 + 1
        move_cursor(row + 1, 1)

    def print_menu(self, active_menu: Menu) -> None:
        chars = [
            self.render.theme_char["corner"][0b0110],
            self.render.theme_char["corner"][0b1100],
            self.render.theme_char["corner"][0b0011],
            self.render.theme_char["corner"][0b1001],
            self.render.theme_char["wall_n"],
            self.render.theme_char["wall_w"],
        ]
        if self.color:
            print_menu_ansi(active_menu, chars, self.render.theme_color)
        else:
            print_menu_ascii(active_menu, chars)

    def quit(self) -> None:
        self.game_over = True
        self.generator.export_maze()
        if self.maze_config.pretty:
            print_goodbye()
        print_line(f"saving output file to {self.maze_config.output_file}\n")
        self.state = MenuState.EXIT

    def _handle_input(self, active_menu: Menu) -> None:
        key = read_menu_key()
        if key is MenuKey.UP:
            active_menu.move_up()
        elif key is MenuKey.DOWN:
            active_menu.move_down()
        elif key is MenuKey.SELECT:
            active_menu.selected_item().action()
        elif key is MenuKey.EXIT:
            if self.state == MenuState.CONFIG_MENU:
                self.state = MenuState.MENU
            elif self.state == MenuState.MENU:
                self.generator.export_maze()
                if self.maze_config.pretty:
                    print_goodbye()
                print_line(
                    f"saving output file to {self.maze_config.output_file}\n"
                )
                sys.exit(0)
        else:
            active_menu.get_item(key).action()
        # IGNORED / QUIT-without-confirmation / anything else -> no-op,
        # loop asks again. This is the actual "block other keys" behavior.

    # ---- actions ---------------------------------------------------

    def show_solution(self) -> None:
        self.render.show_solution = not self.render.show_solution
        clear_screen(self.color)
        self.render.print_grid()

    def clear_print(self) -> None:
        clear_screen(self.color)
        self.render.print_grid()

    def open_config_menu(self) -> None:
        if not self.config_menu:
            self.config_menu = Menu(
                name="Edit A-Maze-Ing Configuration",
                items=[
                    MenuItem(
                        "I",
                        "Width",
                        {"I", "i"},
                        lambda: self.edit_config("width"),
                    ),
                    MenuItem(
                        "H",
                        "Height",
                        {"H", "h"},
                        lambda: self.edit_config("height"),
                    ),
                    MenuItem(
                        "P",
                        "Perfect",
                        {"P", "p"},
                        lambda: self.edit_config("perfect"),
                    ),
                    MenuItem(
                        "A",
                        "Algorithm",
                        {"A", "a"},
                        lambda: self.edit_config("algorithm"),
                    ),
                    MenuItem(
                        "S",
                        "Solution Algorithm",
                        {"S", "s"},
                        lambda: self.edit_config("solution_algorithm"),
                    ),
                    MenuItem(
                        "O",
                        "Output file",
                        {"O", "o"},
                        lambda: self.edit_config("output_file"),
                    ),
                    MenuItem(
                        "E",
                        "Entry",
                        {"E", "e"},
                        lambda: self.edit_config("entry"),
                    ),
                    MenuItem(
                        "X",
                        "Exit",
                        {"X", "x"},
                        lambda: self.edit_config("exit"),
                    ),
                    MenuItem(
                        "F",
                        "Color",
                        {"F", "f"},
                        lambda: self.edit_config("color"),
                    ),
                    MenuItem(
                        "T",
                        "Theme characters",
                        {"T", "t"},
                        lambda: self.edit_config("theme_char"),
                    ),
                    MenuItem(
                        "L",
                        "Theme color",
                        {"L", "l"},
                        lambda: self.edit_config("theme_color"),
                    ),
                    MenuItem(
                        "D",
                        "Delay",
                        {"D", "d"},
                        lambda: self.edit_config("delay"),
                    ),
                    MenuItem(
                        "R",
                        "Seed",
                        {"R", "r"},
                        lambda: self.edit_config("seed"),
                    ),
                    MenuItem(
                        "Z",
                        "Cell size",
                        {"Z", "z"},
                        lambda: self.edit_config("cell_size"),
                    ),
                ],
            )
        self.state = MenuState.CONFIG_MENU

    def generate_new_maze(self) -> None:
        if self.maze_config.animated:
            self.generator.on(
                "cell_updated",
                lambda **kwargs: self.render.render(
                    maze=kwargs["maze"],
                    info=kwargs["info"],
                ),
            )
        else:
            self.generator.on(
                "maze_completed",
                lambda **kwargs: self.render.render(
                    maze=kwargs["maze"],
                    info=None,
                ),
            )
        self.generator.on(
            "maze_completed",
            lambda **kwargs: self.render.render_clean_up(**kwargs),
        )
        self.generator.on(
            "maze_solution",
            lambda **kwargs: self.render.update_context(**kwargs),
        )
        self.generator.seed = (self.generator.seed or 0) + 1
        self.render.solution_set = set()
        self.generator.generate()

    def enter_play_mode(self) -> None:
        if not self.play_manager:
            self.play_manager = PlayManager(
                self.maze_config,
                self.generator,
                self.render,
            )
        self.play_manager.game_over = False
        self.play_manager.run()

    # ---- config_menu actions ----------------------------------------------
    def edit_config(self, name: str) -> None:
        """
        Used to update width, height or other integer values
        of the maze configuration, then it creates
        a new maze generator.
        Finally, generate the maze again.
        """

        self._cursor_after_maze()
        regenerate = True
        redirect_coords = False
        if name in ("perfect", "pretty", "animated", "color"):
            self._cursor_after_maze()
            clear_from_cursor()
            new_value = read_boolean_key()
            if (
                name == "perfect" and not new_value
            ) or name in ("pretty", "color"):
                regenerate = False
        else:
            try:
                if name in ("width", "height", "seed", "delay", "cell_size"):
                    raw_value = self.print_edit_config_input(name)
                    new_value = int(raw_value)
                    if name in ("width", "height"):
                        redirect_coords = True
                    else:
                        regenerate = False
                elif name in ("entry", "exit"):
                    raw_value = self.print_edit_config_input(name)
                    new_value = str_to_coords(raw_value)
                    if self.generator.maze.get_cell(
                        new_value[0], new_value[1]
                    ).blocked:
                        raise ValueError(
                            f"The coordinate used {new_value} is blocked"
                        )
                elif name in ("config_file", "output_file"):
                    new_value = self.print_edit_config_input(name)
                    regenerate = False
                elif name == "algorithm":
                    self._cursor_after_maze()
                    clear_from_cursor()
                    new_value = read_algorithm_key()
                elif name == "solution_algorithm":
                    self._cursor_after_maze()
                    clear_from_cursor()
                    new_value = read_sol_algorithm_key()
                elif name == "theme_char":
                    self._cursor_after_maze()
                    clear_from_cursor()
                    new_value = read_theme_char_key()
                    self.render.theme_char = get_theme_chars(new_value)
                elif name == "theme_color":
                    self._cursor_after_maze()
                    clear_from_cursor()
                    new_value = read_theme_color_key()
                    self.render.theme_color = get_theme_colors(new_value)
            except ValueError as exc:
                msg = (
                    "Error, inserted invalid value for maze attribute "
                    f"'{name}': {new_value}"
                )
                print(msg, file=sys.stderr)
                print(
                    f"Raised the following exception: {exc}",
                    file=sys.stderr,
                )
                regenerate = False

        # Update all fields shared between config and generator.
        # Then, create a new render re-initialized with the new maze.
        # New config -> new generator -> new render.
        try:
            self.maze_config = self.maze_config.update_config(name, new_value)
            if redirect_coords:
                self.maze_config.redirect_entries()
            gen_data = self.generator.model_dump()
            config_data = self.maze_config.model_dump()
            shared = set(gen_data) & set(config_data)
            gen_data.update({k: config_data[k] for k in shared})
            self.generator = type(self.generator)(**gen_data)
            self.maze_config_setup(name)
        except ValidationError as exc:
            msg = (
                "ValidationError while editing config attribute "
                f"'{name}': {new_value}"
            )
            print(msg, file=sys.stderr)
            print(f"Raised the following exception: {exc}", file=sys.stderr)
            regenerate = False

        self._close_config_menu(regenerate)

    def print_edit_config_input(self, name: str) -> str:
        self._cursor_after_maze()
        clear_from_cursor()
        if self.color:
            print_menu_lines_ansi(
                "Maze Configuration Edit",
                [f"Insert the new value for {name} please: "],
                self.render.theme_char,
                self.render.theme_color,
                self.render.cell_size,
            )
        else:
            print_menu_lines_ascii(
                "Maze Configuration Edit",
                [f"Insert the new value for {name} please: "],
                self.render.theme_char,
                self.render.cell_size,
            )
        print(" >> ", end="", flush=True)
        user_input = sys.stdin.readline()
        return user_input

    def maze_config_setup(self, name: str) -> None:
        """
        This function executes setup for the config once validations have
        already passed. The tasks may change depending on which attribute was
        changed, indicated by "name".

        Parameters
        ----------
        name: str
            which attribute was changed
        """
        if self.maze_config.animated:
            self.generator.on(
                "cell_updated",
                lambda **kwargs: self.render.render(
                    kwargs["maze"],
                    kwargs["info"],
                ),
            )
        else:
            self.generator.on(
                "maze_completed",
                lambda **kwargs: self.render.render(
                    kwargs["maze"],
                    kwargs["info"],
                ),
            )
        self.generator.on(
            "completed",
            lambda **kwargs: self.render.render_clean_up(),
        )
        self.generator.on(
            "maze_solution",
            lambda **kwargs: self.render.update_context(**kwargs),
        )
        if name == "perfect":
            if not self.maze_config.perfect:
                self.generator.make_imperfect(self.generator.maze)
        elif name == "color":
            self.render.color = self.maze_config.color
            self.color = self.maze_config.color
        elif name == "delay":
            self.render.set_frame_delay(self.maze_config.delay)
        elif name == "cell_size":
            self.render.set_cell_size(self.maze_config.cell_size)

    def _close_config_menu(self, regenerate: bool = False) -> None:
        self.state = MenuState.MENU
        if regenerate:
            self.render.solution_set = set()
            self.generator.generate()
