import random
import sys
from time import sleep
from typing import Any, cast

from exception.render_exception import RenderError
from mazegen import Maze
from render.ascii.constants import (
    MOVE_DELTAS,
    RENDER_THEMES_CHARS,
    RENDER_THEMES_COLORS,
    ThemeChar,
)
from render.ascii.grid import has_wall, wall_go_to
from .utils import (
    cursor_home,
    hex_to_ansi_bg,
    hex_to_ansi_fg,
    hide_cursor,
    show_cursor,
)
from ..base import MazeRenderer


class MazeRendererASCII(MazeRenderer):
    def __init__(self) -> None:
        super().__init__()
        self.width: int = 0
        self.height: int = 0
        self.cell_size: int = 3
        self.entry: tuple[int, int] | None = None
        self.exit: tuple[int, int] | None = None
        self.grid_width: int = 0
        self.grid_height: int = 0
        self.digits: list[str] = []
        self._render_count: int = 0
        self._frame_delay: float = 0.025
        self.context: dict[str, Any] = dict()
        self.solution_set: set[tuple[int, int]] = set()
        self.coin_set: set[tuple[int, int]] = set()
        self.player_pos: tuple[int, int] = (0, 0)
        self.theme_char: ThemeChar = RENDER_THEMES_CHARS["curved"]
        self.theme_color: dict[str, str] = RENDER_THEMES_COLORS["pacman"]
        self.play_mode: bool = False
        self.color: bool = False
        self.show_solution: bool = False
        self.fly_mode: bool = False
        self.blocked_cells: set[tuple[int, int]] = set()

    def set_frame_delay(self, value: float) -> None:
        self._frame_delay = min(max(value, 0.0), 30.0)

    def set_maze_generated(self, value: bool) -> None:
        self._maze_generated = value

    def render(
        self,
        maze: "Maze",
        info: dict[str, Any] | None = None,
    ) -> None:
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
        self.entry = maze.entry
        if self.player_pos is None:
            self.player_pos = self.entry
        self.exit = maze.exit
        self.blocked_cells = maze.blocked_cells
        self.height = len(self.digits)
        self.width = len(self.digits[0]) if self.height > 0 else 0
        self.init_context(info)
        self._build_display_grid()
        self._cell_state_mask = self._build_cell_state_mask()
        self.print_grid()
        if self._frame_delay > 0:
            sleep(self._frame_delay)

    def init_context(self, info: dict[str, Any] | None = None) -> None:
        if info is None:
            self.context = self.default_render_context()
            return
        self.context["current"] = info.get("current", None)
        self.context["hunt_pos"] = info.get("hunt_pos", None)
        self.context["visited"] = info.get("visited", ())
        self.context["solution"] = info.get("solution", ())
        self.context["solution_path"] = info.get("solution_path", "")

    def init_coins(self) -> None:
        coins_count = random.randint(
            self.height,
            self.height // 2 * self.width // 2,
        )
        for _ in range(0, coins_count + 1):
            coord = (
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1),
            )
            self.coin_set.add(coord)

    def default_render_context(self) -> dict[str, Any]:
        return {
            "current": None,
            "hunt_pos": None,
            "visited": set(),
            "solution": set(),
            "solution_path": "",
        }

    def update_context(self, **kwargs: Any) -> None:
        self.context["current"] = kwargs.get("current", None)
        self.context["hunt_pos"] = kwargs.get("hunt_pos", None)
        self.context["visited"] = kwargs.get("visited", ())
        self.context["solution"] = kwargs.get("solution", ())
        self.context["solution_path"] = kwargs.get("solution_path", "")
        self.init_coins()
        self._cell_state_mask = self._build_cell_state_mask()

    def print_grid(self) -> None:
        if self.color:
            self._print_grid_colorized()
        else:
            self._print_grid()

    def render_clean_up(self, **kwargs: Any) -> None:
        # re-set room interiors to be spaces only if no color
        # cursor_home()
        maze = kwargs.get("maze")
        if maze is None:
            print(
                "No maze to execute render clean_up function",
                file=sys.stderr,
            )
        self._cell_state_mask = self._build_cell_state_mask()
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
        wall_n = cast(str, self.theme_char["wall_n"]) * self.cell_size
        wall_w = cast(str, self.theme_char["wall_w"])
        space = cast(str, self.theme_char["space"]) * self.cell_size

        # corners
        for cy in range(self.height + 1):
            for cx in range(self.width + 1):
                idx = 0
                for bit, d in ((1, "N"), (2, "E"), (4, "S"), (8, "W")):
                    if wall_go_to(
                        self.digits,
                        cx,
                        cy,
                        self.width,
                        self.height,
                        d,
                    ):
                        idx |= bit
                grid[cy * 2][cx * 2] = theme["corner"][idx]
                is_wall[cy * 2][cx * 2] = idx != 0

        # horizontal edges (N walls per row, plus the S walls of the last row)
        for gy, source_y, side in (
            [(y * 2, y, "N") for y in range(self.height)]
            + [(self.height * 2, self.height - 1, "S")]
        ):
            row = self.digits[source_y]
            for x in range(self.width):
                walled = has_wall(row[x], side)
                grid[gy][x * 2 + 1] = wall_n if walled else space
                is_wall[gy][x * 2 + 1] = walled

        # vertical edges (W walls per column, plus the E wall of the last
        # column)
        for y in range(self.height):
            row = self.digits[y]
            for gx, side in (
                [(x * 2, "W") for x in range(self.width)]
                + [(self.width * 2, "E")]
            ):
                check_x = gx // 2 if side == "W" else self.width - 1
                walled = has_wall(row[check_x], side)
                grid[y * 2 + 1][gx] = wall_w if walled else " "
                is_wall[y * 2 + 1][gx] = walled

        # room interiors
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == self.player_pos \
                    and self.play_mode \
                        and self.entry != self.player_pos:
                    char = cast(str, theme["player"])
                elif (x, y) == self.entry:
                    char = cast(str, theme["entry"])
                elif (x, y) == self.exit:
                    char = cast(str, theme["exit_"])
                else:
                    char = space
                cell_char = self._center_char(char)
                grid[y * 2 + 1][x * 2 + 1] = cell_char

        self.display_grid = grid
        self.wall_mask = is_wall

    def _build_cell_state_mask(self) -> list[list[str | None]]:
        mask: list[list[str | None]] = [
            [None] * self.width for _ in range(self.height)
        ]

        for (x, y) in self.context.get("solution", ()):
            mask[y][x] = "solution"
            self.solution_set.add((x, y))

        for (x, y) in self.context.get("visited", ()):
            mask[y][x] = "visited"

        for (x, y) in self.coin_set:
            if mask[y][x] is None and (x, y) not in self.blocked_cells:
                mask[y][x] = "coin"

        current = self.context.get("current", None)
        if current:
            mask[current[1]][current[0]] = "current"

        hunt_pos = self.context.get("hunt_pos", None)
        if hunt_pos:
            mask[hunt_pos[1]][hunt_pos[0]] = "hunt_pos"

        if self.entry and self.context.get("solution"):
            mask[self.entry[1]][self.entry[0]] = "entry"

        if self.exit and self.context.get("solution"):
            mask[self.exit[1]][self.exit[0]] = "exit"

        return mask

    def _print_grid(self) -> None:
        h = len(self.display_grid)
        w = len(self.display_grid[0])
        space = cast(str, self.theme_char["space"]) * self.cell_size
        blocked = cast(str, self.theme_char["blocked"]) * self.cell_size
        for y in range(h):
            line = []
            for x in range(w):
                ch = self.display_grid[y][x]
                is_wall = self.wall_mask[y][x]
                if is_wall:
                    line.append(ch)
                    continue
                if y % 2 == 1 and x % 2 == 1:
                    state = self._cell_state_mask[y // 2][x // 2]
                    if state == "current":
                        char = cast(str, self.theme_char.get("current", space))
                        line.append(self._center_char(char))
                        continue
                    elif state == "visited":
                        char = cast(str, self.theme_char.get("visited", space))
                        line.append(self._center_char(char))
                        continue
                    elif state == "hunt_pos":
                        char = cast(
                            str,
                            self.theme_char.get("hunt_pos", space)
                            )
                        line.append(self._center_char(char))
                        continue
                    elif state == "coin" and self.play_mode:
                        char = cast(str, self.theme_char.get("coin", space))
                        line.append(self._center_char(char))
                        continue
                    elif (
                        self.player_pos == ((x - 1) // 2, (y - 1) // 2)
                        and self.play_mode
                    ):
                        char = cast(str, self.theme_char.get("player", space))
                        line.append(self._center_char(char))
                        continue
                    elif (
                        ((x - 1) // 2, (y - 1) // 2) in self.solution_set
                        and self.show_solution
                        and ((x - 1) // 2, (y - 1) // 2) != self.entry
                        and ((x - 1) // 2, (y - 1) // 2) != self.exit
                    ):
                        char = cast(
                            str,
                            self.theme_char.get("solution", space)
                            )
                        line.append(self._center_char(char))
                        continue
                    is_blocked = (
                        self.wall_mask[y + 1][x]
                        and self.wall_mask[y - 1][x]
                        and self.wall_mask[y][x + 1]
                        and self.wall_mask[y][x - 1]
                    )
                    if is_blocked:
                        ch = blocked
                line.append(ch)
            print("".join(line))

    def _print_grid_colorized(self) -> None:
        way_bg = hex_to_ansi_bg(self.theme_color["way"])
        wall_fg = hex_to_ansi_fg(self.theme_color["wall"])
        visited_bg = hex_to_ansi_bg(
            self.theme_color.get("visited", self.theme_color["way"])
        )
        current_bg = hex_to_ansi_bg(
            self.theme_color.get("current", self.theme_color["way"])
        )
        solution_bg = hex_to_ansi_bg(
            self.theme_color.get("solution", self.theme_color["way"])
        )
        h = len(self.display_grid)
        w = len(self.display_grid[0])
        for y in range(h):
            line = []
            for x in range(w):
                ch = self.display_grid[y][x]
                is_wall = self.wall_mask[y][x]
                reset = "\033[0m"
                if is_wall:
                    line.append(f"{wall_fg}{ch}{reset}")
                    continue
                elif y % 2 == 1 and x % 2 == 1:
                    state = self._cell_state_mask[y // 2][x // 2]
                    if state == "current":
                        line.append(f"{current_bg}{ch}{reset}")
                        continue
                    elif state == "visited":
                        line.append(f"{visited_bg}{ch}{reset}")
                        continue
                    elif state == "solution" and self.show_solution:
                        line.append(f"{solution_bg}{ch}{reset}")
                        continue
                    elif state == "player" and self.play_mode:
                        ch = cast(str, self.theme_char["player"])
                        ch = self._center_char(ch)
                        line.append(f"{way_bg}{ch}{reset}")
                        continue
                    elif state == "coin" and self.play_mode:
                        ch = cast(str, self.theme_char["hunt_pos"])
                        ch = self._center_char(ch)
                        line.append(f"{way_bg}{ch}{reset}")
                        continue
                    else:
                        is_blocked = (
                            self.wall_mask[y + 1][x]
                            and self.wall_mask[y - 1][x]
                            and self.wall_mask[y][x + 1]
                            and self.wall_mask[y][x - 1]
                        )
                        bg = (
                            hex_to_ansi_bg(self.theme_color["blocked"])
                            if is_blocked
                            else way_bg
                        )
                        line.append(f"{bg}{ch}{reset}")
                        continue
                line.append(f"{way_bg}{ch}{reset}")
            print("".join(line))

    def _center_char(self, ch: str) -> str:
        center_value = self.cell_size - len(ch)
        return ch.center(center_value, " ")

    # ---------------- moving the player ------------
    def set_player_pos(self, dir: str) -> bool:
        if dir not in MOVE_DELTAS:
            return False

        x, y = self.player_pos
        current_digit = self.digits[y][x]

        if has_wall(current_digit, dir):
            return False

        dx, dy = MOVE_DELTAS[dir]
        new_x = x + dx
        new_y = y + dy
        if not (0 <= new_x < self.width and 0 <= new_y < self.height):
            return False

        self.player_pos = (new_x, new_y)
        self._cell_state_mask[new_y][new_x] = "player"
        if self._cell_state_mask[y][x] == "player":
            self._cell_state_mask[y][x] = None
        return True
