import sys
from time import sleep
from turtle import fd
from typing import Any
from mazegen import Maze
from exception.render_exception import RenderError
from render.ascii.constants import RENDER_THEMES_CHARS, RENDER_THEMES_COLORS
from render.ascii.grid import has_wall, wall_go_to
from .utils import cursor_home, hex_to_ansi_bg, hex_to_ansi_fg, hide_cursor, show_cursor
from ..base import MazeRenderer


class MazeRendererASCII(MazeRenderer):
    def __init__(self) -> None:
        super().__init__()
        self.width: int = 0
        self.height: int = 0
        self.grid_width: int = 0
        self.grid_height: int = 0
        self.digits: list[str] = 0
        self.show_solution: bool = False
        self.play_mode: bool = False
        self.player_pos: tuple[int, int] = (0, 0)
        self.theme_char: dict[str, str] = RENDER_THEMES_CHARS["block"]
        self.theme_color: dict[str, str] = RENDER_THEMES_COLORS["classic"]
        self.color: bool = False
        self._frame_delay: float = 0.025
        self._maze_generated: bool = False
        self._render_count: int = 0
        self.context: dict[str, Any] = dict()

    def set_frame_delay(self, value: float):
        self._frame_delay = min(max(value, 0.0), 30.0)

    def set_maze_generated(self, value: bool):
        self._maze_generated = value

    def render(self, maze: "Maze", info: dict[str, Any] | None = None) -> None:
        if not sys.stdout.isatty():
            raise RenderError(
                "No TTY attached to stdout — this renderer requires an "
                "interactive terminal (stdout is being redirected or piped)."
            )
        self._render_count += 1
        if self._render_count == 1:
            hide_cursor()
        cursor_home()
        self.digits = maze.hex_digits
        self.height = len(self.digits)
        self.width = len(self.digits[0]) if self.height > 0 else 0
        self.init_context(info)
        self._build_display_grid()
        self._cell_state_mask = self._build_cell_state_mask()
        print(f"{self._cell_state_mask}", file=sys.stderr)
        self.print_grid()
        if self._frame_delay > 0:
            sleep(self._frame_delay)

    def init_context(self, info: dict[str, Any] | None = None) -> None:
        if not info:
            self.context = self.default_render_context()
            return
        self.context["current"] = info.get("current", None)
        self.context["hunt_pos"] = info.get("hunt_pos", None)
        self.context["visited"] = info.get("visited", ())
        self.context["solution"] = info.get("solution", ())
        self.context["solution_path"] = info.get("solution_path", "")

    def default_render_context(self) -> dict[str, Any]:
        return {
            "current": None,
            "hunt_pos": None,
            "visited": set(),
            "solution": set(),
            "solution_path": ""
        }

    def print_grid(self) -> None:
        if self.color:
            self._print_grid_colorized()
        else:
            self._print_grid()

    def render_clean_up(self) -> None:
        # re-set room interiors to be spaces only if no color
        # cursor_home()
        if self.color:
            self._print_grid_colorized()
        else:
            self._print_grid()
        show_cursor()

    def _build_display_grid(self) -> None:
        self.grid_height = self.height * 2 + 1
        self.grid_width = self.width * 2 + 1
        rows, cols = self.grid_height, self.grid_width
        grid = [["" for _ in range(cols)] for _ in range(rows)]
        is_wall = [[False for _ in range(cols)] for _ in range(rows)]
        theme = self.theme_char

        # corners
        for cy in range(self.height + 1):
            for cx in range(self.width + 1):
                idx = 0
                for bit, d in ((1, "N"), (2, "E"), (4, "S"), (8, "W")):
                    if wall_go_to(self.digits, cx, cy, self.width, self.height, d):
                        idx |= bit
                grid[cy * 2][cx * 2] = theme["corner"][idx]
                is_wall[cy * 2][cx * 2] = idx != 0

        # horizontal edges (N walls per row, plus the S walls of the last row)
        for gy, source_y, side in [(y * 2, y, "N") for y in range(self.height)] + [(self.height * 2, self.height - 1, "S")]:
            row = self.digits[source_y]
            for x in range(self.width):
                walled = has_wall(row[x], side)
                grid[gy][x * 2 + 1] = theme["wall_n"] if walled else " " * len(theme["wall_n"])
                is_wall[gy][x * 2 + 1] = walled

        # vertical edges (W walls per column, plus the E wall of the last column)
        for y in range(self.height):
            row = self.digits[y]
            for gx, side in [(x * 2, "W") for x in range(self.width)] + [(self.width * 2, "E")]:
                check_x = gx // 2 if side == "W" else self.width - 1
                walled = has_wall(row[check_x], side)
                grid[y * 2 + 1][gx] = theme["wall_w"] if walled else " "
                is_wall[y * 2 + 1][gx] = walled

        # room interiors
        for y in range(self.height):
            for x in range(self.width):
                cell_char = theme["space"]
                grid[y * 2 + 1][x * 2 + 1] = cell_char

        self.display_grid = grid
        self._wall_mask = is_wall

    def _build_cell_state_mask(self) -> list[list[str | None]]:
        mask: list[list[str | None]] = [[None] * self.width for _ in range(self.height)]

        for (x, y) in self.context.get("solution", ()):
            mask[y][x] = "solution"

        for (x, y) in self.context.get("visited", ()):
            mask[y][x] = "visited"

        hunt_pos = self.context.get("hunt_pos", None)
        if hunt_pos:
            mask[hunt_pos[1]][hunt_pos[0]] = "hunt_pos"

        current = self.context.get("current", None)
        if current:
            mask[current[1]][current[0]] = "current"   # applied last → wins ties

        return mask

    def update_context(self, **kwargs: dict[str, Any]) -> None:
        self.context["current"] = kwargs.get("current", None)
        self.context["hunt_pos"] = kwargs.get("hunt_pos", None)
        self.context["visited"] = kwargs.get("visited", ())
        self.context["solution"] = kwargs.get("solution", ())
        self.context["solution_path"] = kwargs.get("solution_path", "")
        self._cell_state_mask = self._build_cell_state_mask()
        print(f"cell state updated {self._cell_state_mask}", file=sys.stderr)

    def _print_grid(self) -> None:
        h = len(self.display_grid)
        w = len(self.display_grid[0])
        for y in range(h):
            line = []
            for x in range(w):
                ch = self.display_grid[y][x]
                is_wall = self._wall_mask[y][x]
                if is_wall:
                    line.append(ch)
                    continue
                if y % 2 == 1 and x % 2 == 1:
                    state = self._cell_state_mask[y // 2][x // 2]
                    if state == "current":
                        line.append(self.theme_char.get("current", self.theme_char["space"]))
                        continue
                    elif state == "visited":
                        line.append(self.theme_char.get("visited", self.theme_char["space"]))
                        continue
                    elif state == "solution":
                        line.append(self.theme_char.get("solution", self.theme_char["space"]))
                        continue
                    elif state == "hunt_pos":
                        line.append(self.theme_char.get("hunt_pos", self.theme_char["space"]))
                        continue
                    is_blocked = self._wall_mask[y + 1][x] \
                        and self._wall_mask[y - 1][x] \
                        and self._wall_mask[y][x + 1] \
                        and self._wall_mask[y][x - 1]
                    if is_blocked:
                        ch = self.theme_char["blocked"]
                line.append(ch)
            print("".join(line))

    def _print_grid_colorized(self) -> None:
        wall_fg = hex_to_ansi_fg(self.theme_color["wall"])
        visited_bg = hex_to_ansi_bg(self.theme_color.get("visited", self.theme_color["way"]))
        current_bg = hex_to_ansi_bg(self.theme_color.get("current", self.theme_color["way"]))
        solution_bg = hex_to_ansi_bg(self.theme_color.get("solution", self.theme_color["way"]))
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
                if y % 2 == 1 and x % 2 == 1:
                    state = self._cell_state_mask[y // 2][x // 2]
                    if state == "current":
                        line.append(f"{current_bg}{ch}{reset}")
                        continue
                    if state == "visited":
                        line.append(f"{visited_bg}{ch}{reset}")
                        continue
                    if state == "solution" and self.show_solution:
                        line.append(f"{solution_bg}{ch}{reset}")
                        continue
                    is_blocked = self._wall_mask[y + 1][x] \
                        and self._wall_mask[y - 1][x] \
                        and self._wall_mask[y][x + 1] \
                        and self._wall_mask[y][x - 1]
                    if is_blocked:
                        fg = hex_to_ansi_bg(self.theme_color["blocked"])
                    else:
                        fg = hex_to_ansi_fg(self.theme_color["way"])
                    ch = f"{fg}{ch}{reset}"
                line.append(ch)
            print("".join(line))
