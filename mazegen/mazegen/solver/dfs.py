from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..model.maze import Maze


def solve_dfs(
    maze: "Maze",
    start: tuple[int, int] | None = None,
    end: tuple[int, int] | None = None,
) -> str:
    start = maze.entry if start is None else start
    end = maze.exit if end is None else end

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
        parent, direction = previous[current]

        path.append(direction)
        current = parent

    path.reverse()

    return "".join(path)
