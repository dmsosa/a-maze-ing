
from mazegen import MazeGenerator

from render.base import MazeRenderer


class MazeRendererASCII(MazeRenderer):
    def __init__(self):
        super().__init__()
        self.play_mode = False

    def render(self, maze: MazeGenerator):
        while (True):
            self.print_maze(maze)

    def print_maze(self, maze: MazeGenerator):
        for y in range(0, maze.height):
            for x in range(0, maze.width):
                print("@")