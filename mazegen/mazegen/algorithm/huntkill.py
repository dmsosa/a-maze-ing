import random

from typing import TYPE_CHECKING


from .base import MazeAlgorithmStrategy
from mazegen.model.maze import Maze

if TYPE_CHECKING:
    from ..model.maze_generator import MazeGenerator


class HuntKillAlgorithm(MazeAlgorithmStrategy):
    """
    Generate a maze using the Hunt-and-Kill algorithm.

    Kill phase:
        Move randomly through unvisited neighboring cells.

    Hunt phase:
        Search for an unvisited cell adjacent to a visited cell
        and connect them.

    Repeat until every cell has been visited.
    """

    def __init__(self, emit_every: int = 1) -> None:
        super().__init__("Hunt and Kill")
        self._visited: set[tuple[int, int]] = set()
        if 0 < emit_every < 25:
            self.emit_every = emit_every
        else:
            self.emit_every = 1
        self._reset_state()

    def generate_algorithm(
        self,
        generator: "MazeGenerator",
        maze: "Maze"
    ) -> None:
        # Bind generated maze to the generator
        self._reset_state()
        self.generator = generator
        self.maze = maze
        visited: set[tuple[int, int]] = set()
        current = maze.entry
        visited.add(current)
        self.total_cells = (
            generator.width * generator.height
            ) - len(generator.blocked_positions)

        current = maze.entry
        visited = visited
        total_cells = self.total_cells

        while len(visited) < total_cells:

            # Kill time
            x, y = current

            unvisited_neighbors = []

            for direction, neighbor in maze.get_available_neighbors(x, y):
                neighbor_position = (neighbor.x, neighbor.y)

                if neighbor_position not in visited:
                    unvisited_neighbors.append((direction, neighbor))

            if unvisited_neighbors:
                direction, neighbor = random.choice(unvisited_neighbors)

                maze.remove_wall(x, y, direction)
                current = (neighbor.x, neighbor.y)
                visited.add(current)
                info = {
                    "visited": visited,
                    "current": current,
                    "hunt_pos": None,
                }
                self._maybe_emit(maze=maze, info=info)
                continue

            # Hunt time
            found = False

            for y in range(maze.height):
                for x in range(maze.width):

                    position = (x, y)

                    cell = maze.get_cell(x, y)

                    if cell.blocked:
                        continue

                    if position in visited:
                        continue

                    visited_neighbors = []

                    for direction, neighbor \
                            in maze.get_available_neighbors(x, y):
                        neighbor_position = (neighbor.x, neighbor.y)

                        if neighbor_position in visited:
                            visited_neighbors.append(
                                (direction, neighbor)
                            )

                    if visited_neighbors:
                        direction, neighbor = random.choice(
                            visited_neighbors
                        )

                        maze.remove_wall(x, y, direction)
                        current = position
                        hunt_pos = position
                        visited.add(current)
                        info = {
                            "visited": visited,
                            "current": current,
                            "hunt_pos": hunt_pos,
                        }
                        self._maybe_emit(maze=maze, info=info)
                        found = True
                        break
                if found:
                    break
