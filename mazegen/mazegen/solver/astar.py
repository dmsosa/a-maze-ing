from typing import TYPE_CHECKING
from .base import MazeSolutionStrategy


if TYPE_CHECKING:
    from ..model.maze import Maze


class AstarSolutionStrategy(MazeSolutionStrategy):
    def __init__(self) -> None:
        super().__init__("A-Star Solution Algorithm")

    def generate_solution(
            self,
            maze: "Maze"
    ) -> tuple[str, set[tuple[int, int]]]:
        solution_path = self._solve_astar(maze)
        solution_coords = self.path_to_coordinates(maze.entry, solution_path)
        return (solution_path, solution_coords)

    def _heuristic(self,
                   current: tuple[int, int],
                   end: tuple[int, int],
                   ) -> int:
        x1, y1 = current
        x2, y2 = end

        return abs(x1 - x2) + abs(y1 - y2)

    def _solve_astar(self, maze: "Maze") -> str:
        """
        Solve a maze using the A* Search algorithm.

        Evaluation phase:
            Select the cell with the lowest estimated total cost.

        Exploration phase:
            Visit open neighboring cells and update their movement cost.

        Path reconstruction:
            Follow the stored previous cells from the exit to the start.

        Return the shortest path as a list of coordinates.
        """

        start = maze.entry
        end = maze.exit

        start_cell = maze.get_cell(*start)
        end_cell = maze.get_cell(*end)

        if start_cell.blocked or end_cell.blocked:
            raise ValueError("Start and end must be available cells")

        open_set = [start]

        g_score = {
            start: 0
        }

        previous: dict[
            tuple[int, int],
            tuple[tuple[int, int], str]
        ] = {}

        while open_set:

            # Evaluation phase
            current = min(
                open_set,
                key=lambda position: (
                    g_score[position]
                    + self._heuristic(position, end)
                ),
            )

            open_set.remove(current)

            if current == end:
                break

            x, y = current

            # Exploration phase
            for direction, neighbor in maze.get_open_neighbors(x, y):
                neighbor_position = (neighbor.x, neighbor.y)

                new_cost = g_score[current] + 1

                if (
                    neighbor_position not in g_score
                    or new_cost < g_score[neighbor_position]
                ):
                    g_score[neighbor_position] = new_cost

                    previous[neighbor_position] = (
                        current,
                        direction.name,
                    )

                    if neighbor_position not in open_set:
                        open_set.append(neighbor_position)

        if end not in g_score:
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
