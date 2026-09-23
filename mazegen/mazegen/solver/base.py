from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from ..model.cell import DELTAS, Direction


if TYPE_CHECKING:
    from ..model.maze import Maze


class MazeSolutionStrategy(ABC):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def path_to_coordinates(
        self,
        entry: tuple[int, int],
        path: str,
    ) -> set[tuple[int, int]]:
        """Walk the direction string from `entry`, collecting every
        cell visited (entry and exit included)."""
        x, y = entry
        coordinates = {(x, y)}

        for char in path:
            dx, dy = DELTAS[Direction[char]]
            x, y = x + dx, y + dy
            coordinates.add((x, y))

        return coordinates

    @abstractmethod
    def generate_solution(
        self,
        maze: "Maze"
    ) -> tuple[str, set[tuple[int, int]]]:
        raise NotImplementedError("SolutionStrategy not implemented")
