from .base import MazeSolutionStrategy
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..model.maze import Maze


class BFSSolutionStrategy(MazeSolutionStrategy):
    def __init__(self) -> None:
        super().__init__("Breadth-First Search Solution Algorithm")

    def generate_solution(self, maze: "Maze") -> tuple[str, set[tuple[int, int]]]:
        solution_path = self._solve_bfs(maze)
        solution_coords = self.path_to_coordinates(maze.entry, solution_path)
        return solution_path, solution_coords

    def _solve_bfs(self, maze: "Maze") -> str:
        """
        Solve a maze using the Breadth-First Search algorithm.

        Exploration phase:
            Visit open neighboring cells level by level using a queue.

        Search phase:
            Continue exploring until the destination is found.

        Path reconstruction:
            Follow the stored previous cells from the exit to the start.

        Return the shortest path as a string of directions.
        """

        start = maze.entry
        end = maze.exit

        start_cell = maze.get_cell(*start)
        end_cell = maze.get_cell(*end)

        if start_cell.blocked or end_cell.blocked:
            raise ValueError("Start and end must be available cells")

        queue = [start]
        index = 0

        visited = {start}

        previous: dict[
            tuple[int, int],
            tuple[tuple[int, int], str]
        ] = {}

        while index < len(queue):

            # Search phase
            x, y = queue[index]
            index += 1

            current = (x, y)

            if current == end:
                break

            # Exploration phase
            for direction, neighbor in maze.get_open_neighbors(x, y):
                neighbor_position = (neighbor.x, neighbor.y)

                if neighbor_position in visited:
                    continue

                visited.add(neighbor_position)

                previous[neighbor_position] = (
                    current,
                    direction.name,
                )

                queue.append(neighbor_position)

        if end not in visited:
            raise ValueError("No path exists between entry and exit")

        # Path reconstruction
        path: list[str] = []
        current = end

        while current != start:
            parent, direction = previous[current]

            path.append(direction)
            current = parent

        path.reverse()

        return "".join(path)
