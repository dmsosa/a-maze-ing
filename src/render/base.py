from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from mazegen import Maze, MazeGenerator


class MazeRenderer(ABC):
    @abstractmethod
    def render(self, maze: "Maze", info: dict[str, Any] | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def render_clean_up(self, **kwargs: dict[str, Any]) -> str:
        raise NotImplementedError
    

    def set_frame_delay(self, value: float) -> None:
        self._frame_delay = min(max(value, 0.0), 10.0)

    def set_maze_generated(self, value: bool) -> None:
        self._maze_generated = value
