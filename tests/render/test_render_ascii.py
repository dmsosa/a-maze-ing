import sys

from mazegen import MazeGenerator
from mazegen.model.cell import Direction
from mazegen.model.constants import MazeAlgorithm
from mazegen.model.maze import Maze
from config.config import MazeConfiguration
from render.ascii.render_ascii import MazeRendererASCII
from render.ascii.utils import clear_screen, cursor_home, move_cursor, move_cursor_right, move_cursor_up, print_char, print_square


CELL_WIDTH = 2


def render_maze(maze: Maze) -> None:
    """
    Render the maze using ASCII/Unicode box-drawing characters.

    Expected Maze interface:

        maze.height
        maze.width
        maze.get_cell(row, col)

    Adapt get_cell() if your Maze uses a different API.
    """

    renderer = MazeRendererASCII()
    clear_screen()
    cursor_home()
    for row in range(maze.height):
        # -------------------------------------------------
        # TOP WALLS
        # -------------------------------------------------

        for col in range(maze.width):
            cell = maze.get_cell(row, col)

            print_square(renderer.active_theme["wall"])
            if cell.has_wall(Direction.N):
                print_square(renderer.active_theme["wall"])
            else:
                print_square(renderer.active_theme["way"])
            move_cursor((row * CELL_WIDTH) + 1)
            if cell.has_wall(Direction.W):
                print_square(renderer.active_theme["wall"])
            if cell.blocked:
                print_square(renderer.active_theme["wall"])
            else:
                print_square(renderer.active_theme["way"])
            print_char("\n")
            move_cursor_up(CELL_WIDTH)
            move_cursor_right(col * CELL_WIDTH)
            sys.stdout.flush()
        print_square(renderer.active_theme["wall"])
        print_char("\n")
        print_square(renderer.active_theme["wall"])
        print_char("\n")


def main():
    # -----------------------------------------------------
    # Replace this with however you construct your maze.
    # -----------------------------------------------------
    config = MazeConfiguration.default_config()
    maze_generator = MazeGenerator(**config.model_dump())
    maze = maze_generator.generate()
    render_maze(maze)


if __name__ == "__main__":
    main()