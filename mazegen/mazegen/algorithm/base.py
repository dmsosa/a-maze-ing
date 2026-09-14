from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..model.maze_generator import MazeGenerator, Maze


class MazeAlgorithmStrategy(ABC):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    @abstractmethod
    def generate_algorithm(self, generator: "MazeGenerator", maze: "Maze") -> None:
        raise NotImplementedError("MazeAlgorithmStrategy not implemented")

    @abstractmethod
    def show(self) -> str:
        pass

    def _reset_state(self) -> None:
        """Must run at the START of every generate_algorithm() call — this
        instance is a shared singleton (see ALGORITHM_MAP), so stale state
        from a PREVIOUS maze would otherwise leak into the next one."""
        self.generator: "MazeGenerator | None" = None
        self.maze: Maze | None = None
        self.visited: set[tuple[int, int]] = set()
        self.current: tuple[int, int] | None = None
        self.hunt_pos: tuple[int, int] | None = None
        self.move_count = 0
        self.total_cells = 0
