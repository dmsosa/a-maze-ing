from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from ..model.maze_generator import MazeGenerator, Maze


class MazeAlgorithmStrategy(ABC):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    @abstractmethod
    def generate_algorithm(self, generator: "MazeGenerator", maze: "Maze") -> None:
        raise NotImplementedError("MazeAlgorithmStrategy not implemented")

    def _reset_state(self) -> None:
        """Must run at the START of every generate_algorithm() call — this
        instance is a shared singleton (see ALGORITHM_MAP), so stale state
        from a PREVIOUS maze would otherwise leak into the next one."""
        self.generator: "MazeGenerator | None" = None
        self.maze: Maze | None = None
        self.visited: set[tuple[int, int]] = set()
        self.current: tuple[int, int] | None = None
        self.hunt_pos: tuple[int, int] | None = None
        self.move_count: int = 0
        self.total_cells: int = 0
        self.emit_every: int = 1

    def _maybe_emit(self, **kwargs: dict[str, Any]) -> None:
        self.move_count += 1
        if self.move_count % self.emit_every == 0:
            self.generator.emit(
                "cell_updated",
                **kwargs,
            )
