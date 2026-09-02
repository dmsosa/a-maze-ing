from .cell import Cell, DELTAS, Direction, OPPOSITE
from typing import List, Tuple
from pydantic import BaseModel, Field
from mazegen.model.constants import MazeAlgorithm
from ..algorithm import get_algorithm


class MazeGenerator(BaseModel):
    """
    MazeGenerator generates a maze, it has a method called
    generate() which uses the algorithm currently setted to
    fill the matrix of cells with cells that have neighbours
    pointing to another cell (in case of having a neighbour
    in that direction, which means that there is a way)
    or NULL (in case of having no neighbour in that direction,
    which means that there is a wall).

    It means generate method is a void function.
    method generate_output traverses our matrix of cells
    and gives as output a matrix of hexadecimal characters,
    useful for generating the output.txt file.

    It can be connected later to the solver package to
    find an array of solutions for the maze.

    Attributes:
        width: int = Field(gt=0, lt=120)
        height: int = Field(gt=0, lt=120)
        cells: 2D array (or Matrix) of cell objects
        entry: Cell where character starts
        exit: Cell where character ends
        algorithm: MazeAlgorithm
        seed: int
        perfect: boolean
        array: List[Cell][Cell]

    :param x: string to print
    :param y: string to print
    :example:
    my_func("hello world!")
    """
    width: int = Field(gt=0, lt=120)
    height: int = Field(gt=0, lt=120)
    cells: List[List[Cell]] = Field(default=[])
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    algorithm: MazeAlgorithm
    seed: int
    perfect: int

    def generate(self):
        strategy = get_algorithm(self.algorithm)
        strategy.generate_algorithm(self)

    def output(self) -> str:
        return "opela"

    def get_cell(self, x: int, y: int) -> Cell:
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError("Coordinates outside the maze")

        return self.cells[y][x]

    def initialize_all_walls(self) -> None:
        for y in range(self.height):
            row: list[Cell] = []
            for x in range(self.width):
                cell = Cell(x=x, y=y)
                row.append(cell)

            self.cells.append(row)

    def get_neighbors(
        self,
        x: int,
        y: int,
    ) -> list[tuple[Direction, Cell]]:
        self.get_cell(x, y)

        neighbors: list[tuple[Direction, Cell]] = []

        for direction in Direction:
            dx, dy = DELTAS[direction]

            neighbor_x = x + dx
            neighbor_y = y + dy

            if (0 <= neighbor_x < self.width
                    and 0 <= neighbor_y < self.height):
                neighbor = self.get_cell(neighbor_x, neighbor_y)
                neighbors.append((direction, neighbor))

        return neighbors

    def remove_wall(
        self,
        x: int,
        y: int,
        direction: Direction,
    ) -> None:
        cell = self.get_cell(x, y)

        dx, dy = DELTAS[direction]
        neighbor = self.get_cell(x + dx, y + dy)

        if cell.blocked or neighbor.blocked:
            raise ValueError("Cannot open a wall of a blocked cell")

        cell.walls[direction] = False
        neighbor.walls[OPPOSITE[direction]] = False
