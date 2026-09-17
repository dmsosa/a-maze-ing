from enum import IntEnum
from pydantic import BaseModel, Field


class Direction(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3


DELTAS: dict[Direction, tuple[int, int]] = {
    Direction.N: (0, -1),
    Direction.E: (1, 0),
    Direction.S: (0, 1),
    Direction.W: (-1, 0),
}

OPPOSITE: dict[Direction, Direction] = {
    Direction.N: Direction.S,
    Direction.E: Direction.W,
    Direction.S: Direction.N,
    Direction.W: Direction.E,
}

WALL_WEIGHTS: dict[Direction, int] = {
    Direction.N: 1,
    Direction.E: 2,
    Direction.S: 4,
    Direction.W: 8,
}


def closed_walls() -> dict[Direction, bool]:
    """Returns a new dictionary: True means a closed wall."""
    walls: dict[Direction, bool] = {}

    for direction in Direction:
        walls[direction] = True

    return walls


class Cell(BaseModel):
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    walls: dict[Direction, bool] = Field(default_factory=closed_walls)
    blocked: bool = False

    def has_wall(self, direction: Direction) -> bool:
        """True means a closed wall"""
        return self.walls[direction]

    def ctoh(self) -> str:
        """Return a character between 0 and F without modifying the cell"""
        value: int = 0
        for direction in Direction:
            if self.has_wall(direction):
                value += WALL_WEIGHTS[direction]
        return format(value, "x")
