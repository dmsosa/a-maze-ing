from abc import ABC, abstractmethod

from mazegen import MazeGenerator


class MazeRenderer(ABC):
    @abstractmethod
    def render(self, maze: MazeGenerator):
        raise NotImplementedError