from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..model.maze import Maze


def heuristic(
    current: tuple[int, int],
    end: tuple[int, int],
) -> int:
    x1, y1 = current
    x2, y2 = end

    return abs(x1 - x2) + abs(y1 - y2)


def solve_astar(maze: "Maze") -> str:
    """
    Solve a maze using the A* Search algorithm.

    Exploration phase:
        Explore open neighboring cells using their estimated cost.

    Evaluation phase:
        Prioritize cells using the distance already traveled
        and the estimated distance to the exit.

    Repeat until the exit is reached, then reconstruct the shortest path.
    """

    start = maze.entry
    end = maze.exit

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
                + heuristic(position, end)
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
        parent, direction = previous[current]

        path.append(direction)
        current = parent

    path.reverse()

    return "".join(path)
