from typing import List, Tuple

from pydantic import BaseModel, Field

from .cell import Cell, DELTAS, Direction, OPPOSITE


class Maze(BaseModel):
    """
    Represents the maze structure.

    Stores the cells and provides methods to access neighbors
    and modify connections between cells.
    """

    width: int = Field(gt=0, lt=500)
    height: int = Field(gt=0, lt=500)
    cells: List[List[Cell]] = Field(default_factory=list)
    blocked_cells: set[tuple[int, int]] = set()
    entry: Tuple[int, int]
    exit: Tuple[int, int]

    def get_cell(self, x: int, y: int) -> Cell:
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(
                f"Coordinates outside the maze: '({x}, {y})',"
                f"{self.model_dump()}"
                )

        return self.cells[y][x]

    def initialize_cells(self) -> None:
        """Creation of the cells. The closed walls are being
        defined by Cell"""
        self.cells.clear()

        for y in range(self.height):
            row: list[Cell] = []

            for x in range(self.width):
                cell = Cell(x=x, y=y)
                row.append(cell)

            self.cells.append(row)

    def set_blocked_cells(self, blocked_cells: set[tuple[int, int]]) -> None:
        self.blocked_cells = blocked_cells

    def get_neighbors(
        self,
        x: int,
        y: int,
    ) -> list[tuple[Direction, Cell]]:
        """All geometric neighbors"""
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

    def get_available_neighbors(
        self,
        x: int,
        y: int,
    ) -> list[tuple[Direction, Cell]]:
        """Neighbors who are NOT blocked"""
        available_neighbors: list[tuple[Direction, Cell]] = []

        for direction, neighbor in self.get_neighbors(x, y):
            if not neighbor.blocked:
                available_neighbors.append((direction, neighbor))

        return available_neighbors

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

    @property
    def hex_digits(self) -> List[str]:
        lines = []

        for row in self.cells:
            line = "".join(cell.ctoh() for cell in row)
            lines.append(line)

        return lines

    def get_open_neighbors(
        self,
        x: int,
        y: int,
    ) -> list[tuple[Direction, Cell]]:
        cell = self.get_cell(x, y)
        """For solver"""

        open_neighbors: list[tuple[Direction, Cell]] = []

        for direction, neighbor in self.get_neighbors(x, y):
            if not cell.walls[direction]:
                open_neighbors.append((direction, neighbor))

        return open_neighbors

    def block_cells(
        self,
        positions: set[tuple[int, int]],
    ) -> None:
        for x, y in positions:
            self.get_cell(x, y).blocked = True
