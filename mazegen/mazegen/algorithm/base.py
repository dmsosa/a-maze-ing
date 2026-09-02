from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from mazegen.model.maze_generator import MazeGenerator


class MazeAlgorithmStrategy(ABC):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    @abstractmethod
    def generate_algorithm(self, maze: "MazeGenerator") -> None:
        raise NotImplementedError("MazeAlgorithmStrategy not implemented")

    @abstractmethod
    def show(self) -> str:
        pass
