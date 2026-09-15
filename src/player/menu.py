# src/player/menu.py
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class MenuItem:
    label: str
    action: Callable[[], None]


@dataclass
class Menu:
    items: list[MenuItem] = field(default_factory=list)
    selected_index: int = 0

    def move_up(self) -> None:
        self.selected_index = (self.selected_index - 1) % len(self.items)

    def move_down(self) -> None:
        self.selected_index = (self.selected_index + 1) % len(self.items)

    def selected_item(self) -> MenuItem:
        return self.items[self.selected_index]

    def labels(self) -> list[str]:
        return [item.label for item in self.items]
