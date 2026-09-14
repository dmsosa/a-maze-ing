from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..model.maze import Maze


def solve_bfs(maze: "Maze") -> str:
    """
    Solve a maze using the Breadth-First Search algorithm.

    Exploration phase:
        Explore open neighboring cells level by level using a queue.

    Search phase:
        Visit all reachable cells in increasing distance from the start.

    Repeat until the exit is reached, then reconstruct the shortest path.
    """
    start = maze.entry
    end = maze.exit

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
