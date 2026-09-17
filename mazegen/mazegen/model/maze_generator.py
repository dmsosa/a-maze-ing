from collections import defaultdict
from typing import Callable, Tuple
from ..solver import get_solution_algorithm
from pydantic import BaseModel, Field, PrivateAttr
from constants import SNAKE_CASE_REGEXP
from .cell import DELTAS, Direction
from .constants import MazeAlgorithm, SolutionAlgorithm
from ..algorithm import get_algorithm
from .maze import Maze
import random
from ..pattern.forty_two import FORTY_TWO_PATTERN
from ..pattern.utils import centered_positions
from .cell import DELTAS, Direction


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
    MazeGenerator generates a maze, it has a method called
    generate() which uses the algorithm currently setted to
    fill the matrix of cells with cells that have neighbours
    pointing to another cell (in case File "/home/durisosa/work/repos-official/deliver-amazeing/./src/a_maze_ing.py", line 67, in main
    maze = maze_generator.generate()
  File "/home/durisosa/work/repos-official/deliver-amazeing/mazegen/mazegen/model/maze_generator.py", line 9 of having a neighbour
    in that direction, which means that there is a way)
    or NULL (in case of having no neighbour in that direction,
    which means that there is a wall).

    It means generate method is a void function.
    method generate_output traverses our matrix of cells
    and gives as output a matrix of hexadecimal characters,
    useful for generating the output.txt file.

    It can be connected later to the solver package to
    find an array of solutions for the maze.

    Coordinates the creation of a maze.

    It creates the Maze structure, initializes its cells,
    selects the generation algorithm and executes it.

    """
    width: int = Field(gt=0, lt=500)
    height: int = Field(gt=0, lt=500)
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    algorithm: MazeAlgorithm = MazeAlgorithm.PRIM
    seed: int | None = None
    perfect: bool = True
    output_file: str = Field(default="output.txt", pattern=SNAKE_CASE_REGEXP)
    solution_algorithm: SolutionAlgorithm = SolutionAlgorithm.ASTAR
    solution_path: str = ""
    solution_coords: set[tuple[int, int]] = set()
    maze: Maze | None = None

    def generate(self) -> "Maze":
        if self.seed is not None:
            random.seed(self.seed)

        self.maze = Maze(**self.model_dump()) 
        self.maze.initialize_cells()

        blocked_positions = centered_positions(
        FORTY_TWO_PATTERN,
        self.maze.width,
        self.maze.height,
        )

        if self.maze.entry in blocked_positions:
            self.maze.entry = (0, 0)

        if self.maze.exit in blocked_positions:
            self.maze.exit = (
                self.maze.width - 1,
                self.maze.height - 1,
            )

        if self.maze.entry == self.maze.exit:
            raise ValueError("Entry and exit cannot be the same cell")

        self.maze.block_cells(blocked_positions)

        strategy = get_algorithm(self.algorithm)
        # Passing self to algorithm itself
        # to be able to emit events while executing
        strategy.generate_algorithm(self, self.maze)
        if not self.perfect:
            self.make_imperfect(self.maze)
        solution_strategy = get_solution_algorithm(self.solution_algorithm)
        solution_path, solution_coords = solution_strategy.generate_solution(self.maze)
        self.solution_path = solution_path
        self.solution_coords = solution_coords
        self.emit(
            "maze_solution",
            solution=solution_coords,
            solution_path=solution_path,
            )
        self.emit("maze_completed", maze=self.maze, info=None)
        return self.maze

    def would_create_open_3x3(
        self,
        maze: "Maze",
        x: int,
        y: int,
        direction: Direction,
    ) -> bool:
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
        candidates: list[tuple[int, int, Direction]] = []
        available_cells = 0

        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)

                if cell.blocked:
                    continue

                available_cells += 1

                for direction, _ in maze.get_available_neighbors(x, y):
                    if direction not in (Direction.E, Direction.S):
                        continue

                    if cell.has_wall(direction):
                        candidates.append((x, y, direction))

        random.shuffle(candidates)

        target_openings = max(1, available_cells // 20)
        opened = 0

        for x, y, direction in candidates:
            if self.would_create_open_3x3(
                maze,
                x,
                y,
                direction,
            ):
                continue

            maze.remove_wall(x, y, direction)
            opened += 1
            self.emit("cell_updated", generator=self, maze=self.maze, info=dict())
            if opened >= target_openings:
                break

        if opened == 0:
            raise ValueError("Could not create an imperfect maze")

    def output_text(self) -> str:
        """Return the output format required by the subject."""

        maze_rows = "\n".join(self.maze.hex_digits)

        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit

        return (
            f"{maze_rows}\n\n"
            f"{entry_x},{entry_y}\n"
            f"{exit_x},{exit_y}\n"
            f"{self.solution_path}\n"
        )

    def export_maze(
        self) -> None:
        """Write a generated maze and its solution to a file."""

        content = self.output_text()

        with open(
            self.output_file,
            "w",
            encoding="utf-8",
            newline="\n",
        ) as file:
            file.write(content)
