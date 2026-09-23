from .base import MazeSolutionStrategy
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..model.maze import Maze


class DFSSolutionStrategy(MazeSolutionStrategy):
    def __init__(self) -> None:
        super().__init__("Depth-First Search Solution Algorithm")

    def generate_solution(
            self,
            maze: "Maze"
    ) -> tuple[str, set[tuple[int, int]]]:
        solution_path = self._solve_dfs(maze)
        solution_coords = self.path_to_coordinates(maze.entry, solution_path)
        return (solution_path, solution_coords)

    def _solve_dfs(self, maze: "Maze") -> str:
        """
        Solve a maze using the Depth-First Search algorithm.

        Exploration phase:
            Move through open neighboring cells using a stack.

        Backtracking phase:
            Return to previous cells when no unvisited path remains.

        Path reconstruction:
            Follow the stored previous cells from the exit to the start.

        Return the path as a list of coordinates.
        """

        start = maze.entry
        end = maze.exit

        start_cell = maze.get_cell(*start)
        end_cell = maze.get_cell(*end)

        if start_cell.blocked or end_cell.blocked:
            raise ValueError("Start and end must be available cells")

        stack = [start]

        visited = {start}

        previous: dict[
            tuple[int, int],
            tuple[tuple[int, int], str]
        ] = {}

        while stack:

            # Exploration
            x, y = stack.pop()

            current = (x, y)

            if current == end:
                break

            for direction, neighbor in maze.get_open_neighbors(x, y):
                neighbor_position = (neighbor.x, neighbor.y)

                if neighbor_position in visited:
                    continue

                visited.add(neighbor_position)

                previous[neighbor_position] = (
                    current,
                    direction.name,
                )

                stack.append(neighbor_position)

            # Backtracking happens automatically through the stack

        if end not in visited:
            raise ValueError("No path exists between entry and exit")

        # Path reconstruction
        path: list[str] = []
        current = end

        while current != start:
            parent, direct = previous[current]

            path.append(direct)
            current = parent

        path.reverse()

        return "".join(path)
