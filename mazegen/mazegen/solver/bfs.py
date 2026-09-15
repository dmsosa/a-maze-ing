from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..model.maze import Maze


def solve_bfs(
    maze: "Maze",
    start: tuple[int, int] | None = None,
    end: tuple[int, int] | None = None,
    ) -> str:
    """
    Find a path using Breadth-First Search.

    By default, solve from the maze entry to the maze exit.
    Custom start and end positions can also be provided.
    """
    start = maze.entry if start is None else start
    end = maze.exit if end is None else end

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
        parent, dir = previous[current]

        path.append(dir)
        current = parent

    path.reverse()

    return "".join(path)
