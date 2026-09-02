from typing import TYPE_CHECKING

from .base import MazeAlgorithmStrategy

if TYPE_CHECKING:
    from ..model.maze_generator import MazeGenerator


class HuntKillAlgorithm(MazeAlgorithmStrategy):
    def __init__(self) -> None:
        super().__init__("")

    def generate_algorithm(self, maze: "MazeGenerator"):
        """
        This algorithm generation is going to be based on
        a while loop, which condition is: while unvisited
        count is not zero, OR unvisited array is empty, why
        I would need to have the exact coordinate of a visited
        cell? Because I need to check if the cell I am currently
        Hw to know if I remove the cell? I remove from unvisited if I visit it.
        If I visit it, then unvisited has no longer that coordinate.
        Or that I iterate through every row
        and managed to find a cell that is
        not NULL, that satisfies the condition of
        not being visited yet. It means that
        """
        print("Executing algorithm for generating maze...")
        print(f"{self.show()}")
        unvisited = {coord for row in maze.cells for coord in row}
        print(unvisited)
        pass

    def show(self):
        return "Executing Hunt and Kill algorithm"
