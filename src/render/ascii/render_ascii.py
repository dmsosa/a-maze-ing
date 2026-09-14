import os
import platform
import sys
from time import sleep
from typing import Any, List, Tuple
from mazegen import Maze, MazeGenerator
from player.constants import BOLD, RESET
from exception.render_exception import RenderError
from player.utils import get_key
from render.ascii.constants import RENDER_THEMES_CHARS, CORNER_CHARS, RENDER_THEMES_COLORS
from render.ascii.grid import has_wall, wall_go_to
from .utils import cursor_home, hex_to_ansi_bg, hex_to_ansi_fg, hide_cursor, show_cursor
from ..base import MazeRenderer





class MazeRendererASCII(MazeRenderer):
    def __init__(self) -> None:
        super().__init__()
        self.cell_size = 3
        self.play_mode = False
        self.player_pos = (0, 0)
        self.theme_char: dict[str, str] = RENDER_THEMES_CHARS["classic"]
        self.theme_color: dict[str, str] = RENDER_THEMES_COLORS["classic"]
        self.color: bool = False
        self._frame_delay: float = 3.0125
        self._maze_generated: bool = False
        self._render_count: int = 0

    def set_frame_delay(self, value: float):
        self._frame_delay = min(max(value, 0.0), 30.0)

    def set_maze_generated(self, value: bool):
        self._maze_generated = value

    def render(self, generator: "MazeGenerator", maze: "Maze", info: dict[str, Any] | None = None) -> None:
        if not sys.stdout.isatty():
            raise RenderError(
                "No TTY attached to stdout — this renderer requires an "
                "interactive terminal (stdout is being redirected or piped)."
            )
        self._render_count += 1
        if self._render_count == 1:
            self.clear_screen()
            hide_cursor()
            generator.on("maze_completed", lambda **kwargs : self.render_clean_up(**kwargs))
        cursor_home()
        self._build_display_grid(maze.hex_digits, info)
        if self.color:
            self._print_grid_colorized(info)
        else:
            self._print_grid()
        if self._frame_delay > 0:
            sleep(self._frame_delay)

    def render_clean_up(self, **kwargs: dict[str, Any]) -> None:
        show_cursor()

    def render_menu(self) -> str:
        return self._menu_ansi() if self.color else self._menu_ascii()

    def _menu_options_text(self) -> list[str]:
        return ["1. Play", "2. Generate a new maze", "3. Exit"]

    def _menu_ascii(self) -> str:
        lines = ["+" + "-" * 35 + "+", "|{:^35}|".format("MENU"), "+" + "-" * 35 + "+"]
        lines += ["| {:<34}|".format(opt) for opt in self._menu_options_text()]
        lines.append("+" + "-" * 35 + "+")
        print("\n".join(lines))
        return self._read_choice()

    def _menu_ansi(self) -> str:
        accent = hex_to_ansi_fg(self.theme_color["special"])
        lines = [f"{accent}+{'-'*35}+{RESET}", f"{accent}|{RESET}{BOLD}{'MENU':^35}{accent}|{RESET}", f"{accent}+{'-'*35}+{RESET}"]
        lines += [f"{accent}| {RESET}{opt:<34}{accent}|{RESET}" for opt in self._menu_options_text()]
        lines.append(f"{accent}+{'-'*35}+{RESET}")
        print("\n".join(lines))
        return self._read_choice()

    def _read_choice(self) -> str:
        while True:
            key = get_key()
            if key in ("1", "2", "3"):
                return key

    def clear_screen(self) -> None:
        """Call this ONCE, before the animation loop starts."""
        if self.color:
            sys.stdout.write("\033[2J\033[H")
        else:
            os.system("cls" if platform.system() == "Windows" else "clear")
        sys.stdout.flush()

    def _build_display_grid(self, digits: list[str], info) -> None:
        height = len(digits)
        width = len(digits[0]) if height else 0
        rows, cols = height * 2 + 1, width * 2 + 1
        grid = [["" for _ in range(cols)] for _ in range(rows)]
        is_wall = [[False for _ in range(cols)] for _ in range(rows)]
        theme = self.theme_char
        theme_color = self.theme_color
        state_mask = self._build_cell_state_mask(width, height, info)

        # corners
        for cy in range(height + 1):
            for cx in range(width + 1):
                idx = 0
                for bit, d in ((1, "N"), (2, "E"), (4, "S"), (8, "W")):
                    if wall_go_to(digits, cx, cy, width, height, d):
                        idx |= bit
                grid[cy * 2][cx * 2] = CORNER_CHARS[idx]
                is_wall[cy * 2][cx * 2] = idx != 0

        # horizontal edges (N walls per row, plus the S walls of the last row)
        for gy, source_y, side in [(y * 2, y, "N") for y in range(height)] + [(height * 2, height - 1, "S")]:
            row = digits[source_y]
            for x in range(width):
                walled = has_wall(row[x], side)
                grid[gy][x * 2 + 1] = theme["wall_n"] if walled else " " * len(theme["wall_n"])
                is_wall[gy][x * 2 + 1] = walled

        # vertical edges (W walls per column, plus the E wall of the last column)
        for y in range(height):
            row = digits[y]
            for gx, side in [(x * 2, "W") for x in range(width)] + [(width * 2, "E")]:
                check_x = gx // 2 if side == "W" else width - 1
                walled = has_wall(row[check_x], side)
                grid[y * 2 + 1][gx] = theme["wall_w"] if walled else " "
                is_wall[y * 2 + 1][gx] = walled

        # room interiors
        for y in range(height):
            for x in range(width):
                state = state_mask[y][x]
                if state:
                    cell_char = theme_color[state]
                else:
                    cell_char = theme["space"]
                grid[y * 2 + 1][x * 2 + 1] = cell_char

        self.display_grid = grid
        self._wall_mask = is_wall
        self._cell_state_mask = state_mask

    def _build_cell_state_mask(self, width: int, height: int, info: dict | None) -> list[list[str | None]]:
        mask: list[list[str | None]] = [[None] * width for _ in range(height)]
        if not info:
            return mask

        for (x, y) in info.get("visited"):
            mask[y][x] = "visited"

        hunt_pos = info.get("hunt_pos")
        if hunt_pos:
            mask[hunt_pos[1]][hunt_pos[0]] = "hunt_pos"

        current = info.get("current")
        if current:
            mask[current[1]][current[0]] = "current"   # applied last → wins ties

        return mask

    def _print_grid(self) -> None:
        for line in self.display_grid:
            print("".join(line))

    def _print_grid_colorized(self, info: dict[str, Any] | None) -> None:
        wall_fg = hex_to_ansi_fg(self.theme_color["wall"])
        # if info:
        #     visited_fg = hex_to_ansi_fg(self.theme_color.get("visited", self.theme_color["way"]))
        #     visited_fg = hex_to_ansi_fg(self.theme_color.get("current", self.theme_color["way"]))
        reset = "\033[0m"
        h = len(self.display_grid)
        w = len(self.display_grid[0])
        for y in range(h):
            line = []
            for x in range(w):
                ch = self.display_grid[y][x]
                is_wall = self._wall_mask[y][x]
                reset = "\033[0m"
                if is_wall:
                    line.append(f"{wall_fg}{ch}{reset}")
                    continue
                else:
                    is_blocked = self._wall_mask[y + 1][x] \
                        and self._wall_mask[y - 1][x] \
                        and self._wall_mask[y][x + 1] \
                        and self._wall_mask[y][x - 1]
                    if is_blocked:
                        bg = hex_to_ansi_bg(self.theme_color["bg"])
                    else: 
                        bg = hex_to_ansi_bg(self.theme_color["way"])
                    ch = f"{bg}{ch}{reset}"
                line.append(ch)
            print("".join(line))

    def _get_cell_char_playable(
            self,
            pos: Tuple[int, int],
            entry,
            exit_
            ) -> str:
            return "   "

    def _get_cell_char(
            self, 
            pos: Tuple[int, int], 
            visited: List[tuple[int, int]] | None = None, 
            current: tuple[int, int] | None = None,
            hunt_pos: tuple[int, int] | None = None) -> str:
            # if self.play_mode:
            #     return self._get_char_cell_playable
            # if current:
            #     if current == pos:
            #         middle += f"{self._fg('current')}   {RESET}"
            # elif visited:
            #     if pos in visited:
            #         middle += f"{self._fg('visited')}   {RESET}"
            # elif hunt_pos:
            #     if pos == hunt_pos:
            #         middle += "   "
            # else:
                return "   "
