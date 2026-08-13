from pydantic import BaseModel, Field
from enum import Enum

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
    def __init__(self, conf: str):
        print("conf f")