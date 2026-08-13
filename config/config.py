from turtle import width

from pydantic import BaseModel, Field


class MazeConfig(BaseModel):
    width: str = Field(gt=0, lt=100)
    height: str = Field(gt=0, lt=100)
    seed: int = Field(default=0, gt=0)
    algorithn: str = Field(default="hunt-and-kill")

class ConfigLoader():
    @staticmethod
    def init_config(config_path: str) -> MazeConfig:
        with open(config_path, 'r') as fc:
            text = fc.read()
            lines = text.split('\n')
            
