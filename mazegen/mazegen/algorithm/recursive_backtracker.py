import random

from typing import TYPE_CHECKING
from .base import MazeAlgorithmStrategy

if TYPE_CHECKING:
    from ..model.maze import Maze
    from ..model.maze_generator import MazeGenerator


class RecursiveBacktrackerAlgorithm(MazeAlgorithmStrategy):

    """
    Generate a maze using the Recursive Backtracker algorithm.

    Forward phase:
        Move randomly through unvisited neighboring cells,
        storing the current path in a stack.

    Backtracking phase:
        When no unvisited neighbors are available,
        return to the previous cell using the stack.

    Repeat until the stack is empty and no unvisited neighbors remain.
    """

    def __init__(self) -> None:
        super().__init__("Recursive Backtracker")

    def generate_algorithm(
        self,
        generator: "MazeGenerator",
        maze: "Maze",
    ) -> None:
        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = []

        current = maze.entry
        visited.add(current)

        while True:
            x, y = current

            unvisited_neighbors = []

            for direction, neighbor in maze.get_available_neighbors(x, y):
                neighbor_position = (neighbor.x, neighbor.y)

                if neighbor_position not in visited:
                    unvisited_neighbors.append((direction, neighbor))

            # Forward phase
            if unvisited_neighbors:
                direction, neighbor = random.choice(unvisited_neighbors)

                stack.append(current)

                maze.remove_wall(x, y, direction)

                current = (neighbor.x, neighbor.y)

                visited.add(current)

                generator.emit("cell_updated", maze=maze)

            # Backtracking phase
            elif stack:
                current = stack.pop()

            else:
                break

    def show(self) -> str:
        return self.name
