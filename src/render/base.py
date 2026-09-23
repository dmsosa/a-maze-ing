from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from render.ascii.constants import ThemeChar

if TYPE_CHECKING:
    from mazegen import Maze


class MazeRenderer(ABC):
    wall_mask: list[list[bool]] = []
    play_mode: bool
    color: bool
    show_solution: bool
    fly_mode: bool
    solution_set: set[tuple[int, int]] = set()
    theme_char: ThemeChar
    theme_color: dict[str, str]
    player_pos: tuple[int, int] | None = None
    entry: tuple[int, int] | None = None
    exit: tuple[int, int] | None = None
    height: int
    width: int

    @abstractmethod
    def render(
                self,
                maze: "Maze",
                info: dict[str, Any] | None = None
            ) -> None:
        raise NotImplementedError

    @abstractmethod
    def print_grid(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_context(self, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def render_clean_up(self, **kwargs: Any) -> None:
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
