from collections import defaultdict
from typing import Callable, Tuple
from pydantic import BaseModel, Field, PrivateAttr
from .cell import DELTAS, Direction
from .constants import MazeAlgorithm
from ..algorithm import get_algorithm
from .maze import Maze
import random
from ..pattern.forty_two import FORTY_TWO_PATTERN
from ..pattern.utils import centered_positions


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
    algorithm: MazeAlgorithm
    seed: int | None = None
    perfect: bool = True
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
        self.emit(
            "maze_completed",
            generator=self,
            maze=self.maze,
            info=None
            )
        return self.maze

    def find_dead_ends(
            self,
            maze: "Maze",
    ) -> list[tuple[int, int]]:
        dead_ends: list[tuple[int, int]] = []

        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)

                if cell.blocked:
                    continue

                if len(maze.get_open_neighbors(x, y)) == 1:
                    dead_ends.append((x, y))

        return dead_ends

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
        loops_added = 0

        while len(self.find_dead_ends(maze)) > 2:
            dead_ends = self.find_dead_ends(maze)
            random.shuffle(dead_ends)

            opened = False

            for x, y in dead_ends:
                cell = maze.get_cell(x, y)

                candidates = [
                    direction
                    for direction, _ in maze.get_available_neighbors(x, y)
                    if (
                        cell.has_wall(direction)
                        and not self.would_create_open_3x3(
                            maze,
                            x,
                            y,
                            direction,
                        )
                    )
                ]

                if not candidates:
                    continue

                direction = random.choice(candidates)

                maze.remove_wall(x, y, direction)

                loops_added += 1
                opened = True
                break

            if not opened:
                break

    def output(self) -> str:
        return "opela"
