from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..model.maze import Maze


def solve_dfs(maze: "Maze") -> str:
    """
    Solve a maze using the Depth-First Search algorithm.

    Exploration phase:
        Move through unvisited open neighbors using a stack.

    Backtracking phase:
        Return to previous cells when no new path is available.

    Repeat until the exit is reached.
    """
    start = maze.entry
    end = maze.exit

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
