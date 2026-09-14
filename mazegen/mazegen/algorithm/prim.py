import random

from typing import TYPE_CHECKING
from .base import MazeAlgorithmStrategy

if TYPE_CHECKING:
    from ..model.maze import Maze
    from ..model.maze_generator import MazeGenerator


class PrimAlgorithm(MazeAlgorithmStrategy):
    """
    Generate a maze using the Randomized Prim algorithm.

    Start phase:
        Begin from the entry cell and mark it as visited.

    Frontier phase:
        Store unvisited cells adjacent to the visited region.

    Expansion phase:
        Choose a random frontier cell, connect it to a random
        visited neighbor, and add its unvisited neighbors to the frontier.

    Repeat until there are no frontier cells left.
    """

    def __init__(self) -> None:
        super().__init__("Randomized Prim")

    def generate_algorithm(
        self,
        generator: "MazeGenerator",
        maze: "Maze",
    ) -> None:
        visited: set[tuple[int, int]] = set()
        frontier: list[tuple[int, int]] = []
        frontier_set: set[tuple[int, int]] = set()

        # Start phase
        current = maze.entry
        visited.add(current)

        x, y = current

        # Initial frontier
        for _, neighbor in maze.get_available_neighbors(x, y):
            position = (neighbor.x, neighbor.y)

            frontier.append(position)
            frontier_set.add(position)

        # Expansion phase
        while frontier:
            index = random.randrange(len(frontier))
            current = frontier.pop(index)
            frontier_set.remove(current)

            x, y = current

            visited_neighbors = []

            for direction, neighbor in maze.get_available_neighbors(x, y):
                position = (neighbor.x, neighbor.y)

                if position in visited:
                    visited_neighbors.append(
                        (direction, neighbor)
                    )

            if not visited_neighbors:
                continue

            direction, _ = random.choice(visited_neighbors)

            maze.remove_wall(x, y, direction)

            visited.add(current)

            # Update frontier
            for _, neighbor in maze.get_available_neighbors(x, y):
                position = (neighbor.x, neighbor.y)

                if (
                    position not in visited
                    and position not in frontier_set
                ):
                    frontier.append(position)
                    frontier_set.add(position)

            generator.emit("cell_updated", maze=maze)

    def show(self) -> str:
        return self.name
