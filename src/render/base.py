from abc import ABC, abstractmethod
from typing import Any


class MazeRenderer(ABC):
    wall_mask: list[list[bool]] = []

    @abstractmethod
    def render(self, info: dict[str, Any] | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def print_grid(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_context(self, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def render_clean_up(self, **kwargs: Any) -> str:
        raise NotImplementedError

    @abstractmethod
    def set_player_pos(self, direction: str) -> bool:
        """Attempt to move the player one cell towards `direction`
        ('N', 'E', 'S' or 'W'). Returns True if the move succeeded
        (no wall blocking it and destination in bounds), False otherwise."""
        raise NotImplementedError

    def set_frame_delay(self, value: float) -> None:
        self._frame_delay = min(max(value, 0.0), 10.0)

    def set_cell_size(self, value: int) -> None:
        self.cell_size = min(max(value, 1), 5)
