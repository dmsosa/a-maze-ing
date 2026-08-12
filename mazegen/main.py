from pydantic import BaseModel, Field

class Cell(BaseModel):
    x: int
    y: int

class MazeGenerator(BaseModel):
    width: int = Field(gt=0, lt=120)
    height: int = Field(gt=0, lt=120)
    entry: Cell
    exit: Cell 
    def __init__(self, conf: str):
        print("conf f")