import random
from collections import defaultdict
from typing import Callable

from pydantic import BaseModel, Field, PrivateAttr
from .constants import SNAKE_CASE_REGEXP

from ..algorithm import get_algorithm
from ..pattern.forty_two import FORTY_TWO_PATTERN
from ..pattern.utils import centered_positions
from ..solver import get_solution_algorithm
from .cell import DELTAS, Direction
from .constants import MazeAlgorithm, SolutionAlgorithm
from .maze import Maze


class EventEmitter(BaseModel):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """
    _listeners: defaultdict[str, list[Callable]] = PrivateAttr(
            default_factory=lambda: defaultdict[str, list[Callable]](list)
        )

    def on(self, event, callback: Callable) -> None:
        """Subscribe a callback to a specific event type."""
        self._listeners[event].append(callback)

    def off(self, event, callback: Callable) -> None:
        """Unsubscribe a callback from a specific event type."""
        self._listeners[event].remove(callback)

    def emit(self, event: str, **data) -> None:
        """Emit an event — only listeners for that type are called."""
        for callback in self._listeners.get(event, []):
            callback(**data)


class MazeGenerator(EventEmitter):
    """
    Coordinates maze generation.

    Creates and initializes the maze, applies the 42 pattern,
    executes the selected generation algorithm, optionally makes
    the maze imperfect, solves it, and stores the solution.
    """
    width: int = Field(gt=0, lt=500)
    height: int = Field(gt=0, lt=500)
    entry: tuple[int, int]
    exit: tuple[int, int]
    algorithm: MazeAlgorithm = MazeAlgorithm.PRIM
    seed: int | None = None
    perfect: bool = True
    output_file: str = Field(default="output.txt", pattern=SNAKE_CASE_REGEXP)
    solution_algorithm: SolutionAlgorithm = SolutionAlgorithm.ASTAR
    solution_path: str = ""
    solution_coords: set[tuple[int, int]] = Field(default_factory=set)
    maze: Maze | None = None
    blocked_positions: set[tuple[int, int]] = set()

    def generate(self) -> "Maze":
        if self.seed is not None:
            random.seed(self.seed)

        self.maze = Maze(**self.model_dump())
        self.maze.initialize_cells()

        self.blocked_positions = centered_positions(
         FORTY_TWO_PATTERN,
         self.maze.width,
         self.maze.height,
        )

        if self.maze.entry in self.blocked_positions:
            self.maze.entry = (0, 0)
            self.maze.exit = (
                self.maze.width - 1,
                self.maze.height - 1,
            )

        if self.maze.exit in self.blocked_positions:
            self.maze.entry = (0, 0)
            self.maze.exit = (
                self.maze.width - 1,
                self.maze.height - 1,
            )

        if self.maze.entry == self.maze.exit:
            raise ValueError("Entry and exit cannot be the same cell")

        self.maze.block_cells(self.blocked_positions)
        self.maze.set_blocked_cells(self.blocked_positions)

        strategy = get_algorithm(self.algorithm)
        # Passing self to algorithm itself
        # to be able to emit events while executing
        strategy.generate_algorithm(self, self.maze)
        if not self.perfect:
            self.make_imperfect(self.maze)
        sol_strategy = get_solution_algorithm(self.solution_algorithm)
        solution_path, solution_coords = \
            sol_strategy.generate_solution(self.maze)
        self.solution_path = solution_path
        self.solution_coords = solution_coords
        self.emit(
            "maze_solution",
            solution=solution_coords,
            solution_path=solution_path,
            )
        self.emit("maze_completed", maze=self.maze, info=None)
        return self.maze

    def _would_create_open_3x3(
        self,
        maze: "Maze",
        x: int,
        y: int,
        direction: Direction,
    ) -> bool:
        """
        Check whether opening a wall would create a comletely open 3x3 area.
        """

        if maze.width < 3 or maze.height < 3:
            return False

        dx, dy = DELTAS[direction]

        neighbor_x = x + dx
        neighbor_y = y + dy

        new_connection = frozenset(
            ((x, y), (neighbor_x, neighbor_y))
        )

        min_x = min(x, neighbor_x)
        max_x = max(x, neighbor_x)
        min_y = min(y, neighbor_y)
        max_y = max(y, neighbor_y)

        for start_y in range(
            max(0, max_y - 2),
            min(min_y, maze.height - 3) + 1,
        ):
            for start_x in range(
                max(0, max_x - 2),
                min(min_x, maze.width - 3) + 1,
            ):
                open_area = True

                # Horizontal connections
                for row in range(start_y, start_y + 3):
                    for col in range(start_x, start_x + 2):
                        connection = frozenset(
                            ((col, row), (col + 1, row))
                        )

                        if connection == new_connection:
                            continue

                        cell = maze.get_cell(col, row)

                        if cell.has_wall(Direction.E):
                            open_area = False
                            break

                    if not open_area:
                        break

                if not open_area:
                    continue

                # Vertical connections
                for row in range(start_y, start_y + 2):
                    for col in range(start_x, start_x + 3):
                        connection = frozenset(
                            ((col, row), (col, row + 1))
                        )

                        if connection == new_connection:
                            continue

                        cell = maze.get_cell(col, row)

                        if cell.has_wall(Direction.S):
                            open_area = False
                            break

                    if not open_area:
                        break

                if open_area:
                    return True

        return False

    def make_imperfect(
        self,
        maze: "Maze",
    ) -> None:
        required_cells = list(dict.fromkeys((
            (0, 0),
            (maze.width - 1, 0),
            (0, maze.height - 1),
            (maze.width - 1, maze.height - 1),
            (maze.width // 2, maze.height // 2),
        )))

        required_positions = set(required_cells)

        dead_ends: list[tuple[int, int]] = []

        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)

                if (
                    not cell.blocked
                    and (x, y) not in required_positions
                    and len(maze.get_open_neighbors(x, y)) == 1
                ):
                    dead_ends.append((x, y))

        random.shuffle(dead_ends)

        added_edges = 0

        # First process the four corners and the maze center,
        # then reduce the remaining dead ends.
        for x, y in required_cells + dead_ends:
            if len(maze.get_open_neighbors(x, y)) != 1:
                continue

            cell = maze.get_cell(x, y)

            neighbor_candidates = [
                (direction, neighbor)
                for direction, neighbor
                in maze.get_available_neighbors(x, y)
                if (
                    cell.has_wall(direction)
                    and not self._would_create_open_3x3(
                        maze,
                        x,
                        y,
                        direction,
                    )
                )
            ]

            random.shuffle(neighbor_candidates)

            if not neighbor_candidates:
                continue

            # Prefer neighbors with fewer open connections.
            direction, _ = min(
                neighbor_candidates,
                key=lambda candidate: len(
                    maze.get_open_neighbors(
                        candidate[1].x,
                        candidate[1].y,
                    )
                ),
            )

            maze.remove_wall(x, y, direction)
            added_edges += 1

            self.emit(
                "cell_updated",
                generator=self,
                maze=maze,
                info=dict(),
            )

        # Starting from a perfect maze (a connected tree),
        # each additional edge creates one independent cycle.
        if added_edges < 2:
            wall_candidates: list[
                tuple[int, int, Direction]
            ] = []

            for y in range(maze.height):
                for x in range(maze.width):
                    cell = maze.get_cell(x, y)

                    if cell.blocked:
                        continue

                    for direction, _ in (
                        maze.get_available_neighbors(x, y)
                    ):
                        if (
                            direction in (
                                Direction.E,
                                Direction.S,
                            )
                            and cell.has_wall(direction)
                        ):
                            wall_candidates.append(
                                (x, y, direction)
                            )

            random.shuffle(wall_candidates)

            for x, y, direction in wall_candidates:
                if self._would_create_open_3x3(
                    maze,
                    x,
                    y,
                    direction,
                ):
                    continue

                maze.remove_wall(x, y, direction)
                added_edges += 1

                self.emit(
                    "cell_updated",
                    generator=self,
                    maze=maze,
                    info=dict(),
                )

                if added_edges >= 2:
                    break

        if added_edges < 2:
            raise ValueError(
                "Cannot create at least two loops "
                "for this maze size"
            )

        if any(
            len(maze.get_open_neighbors(x, y)) < 2
            for x, y in required_cells
        ):
            raise ValueError(
                "Cannot open every corner and "
                "the maze centre safely"
            )

        remaining_dead_ends = 0

        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)

                if (
                    not cell.blocked
                    and len(maze.get_open_neighbors(x, y)) == 1
                ):
                    remaining_dead_ends += 1

        if remaining_dead_ends > 2:
            raise ValueError(
                "Cannot reduce the imperfect maze "
                "to at most two dead-ends"
            )

    def output_text(self) -> str:
        """Return the output format required by the subject."""

        if self.maze is None:
            raise ValueError("Maze has not been generated")

        maze_rows = "\n".join(self.maze.hex_digits)

        entry_x, entry_y = self.maze.entry
        exit_x, exit_y = self.maze.exit

        return (
            f"{maze_rows}\n\n"
            f"{entry_x},{entry_y}\n"
            f"{exit_x},{exit_y}\n"
            f"{self.solution_path}\n"
        )

    def export_maze(self) -> None:
        """Write a generated maze and its solution to a file."""

        content = self.output_text()

        with open(
            self.output_file,
            "w",
            encoding="utf-8",
            newline="\n",
        ) as file:
            file.write(content)
