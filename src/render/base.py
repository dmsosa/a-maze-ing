from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from mazegen import Maze


class MazeRenderer(ABC):
    @abstractmethod
    def render(self, maze: "Maze") -> None:
        raise NotImplementedError

    @abstractmethod
    def print_grid(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_context(self, **kwargs: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def render_clean_up(self) -> str:
        raise NotImplementedError
    
    def set_frame_delay(self, value: float) -> None:
        self._frame_delay = min(max(value, 0.0), 10.0)


