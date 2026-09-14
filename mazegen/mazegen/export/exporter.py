from ..model.maze import Maze


def output_text(maze: Maze, directions: str) -> str:
    entry_x, entry_y = maze.entry
    exit_x, exit_y = maze.exit

    return (
        f"{maze.hex_digits}\n\n"
        f"{entry_x},{entry_y}\n"
        f"{exit_x},{exit_y}\n"
        f"{directions}\n"
    )


def export_maze(
    maze: Maze,
    directions: str,
    filename: str,
) -> None:
    with open(filename, "w") as file:
        file.write(output_text(maze, directions))
