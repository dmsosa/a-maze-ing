from enum import Enum
from pydantic import BaseModel, Field


class MazeAlgorithm(Enum):
    DFS = "DFS"
    HUNT_N_KILL = "HUNT_AND_KILL"


class CellStatus(Enum):
    EMPTY = 0
    WALL = 1


class Cell(BaseModel):
    x: int
    y: int
    value: CellStatus


class MazeGenerator(BaseModel):
    width: int = Field(gt=0, lt=120)
    height: int = Field(gt=0, lt=120)
    entry: Cell
    exit: Cell
    algo: MazeAlgorithm
