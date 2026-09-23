from ..model.constants import SolutionAlgorithm
from .base import MazeSolutionStrategy
from .astar import AstarSolutionStrategy
from .bfs import BFSSolutionStrategy
from .dfs import DFSSolutionStrategy

SOLUTION_ALGORITHM_MAP: dict[SolutionAlgorithm, MazeSolutionStrategy] = {
    SolutionAlgorithm.ASTAR: AstarSolutionStrategy(),
    SolutionAlgorithm.DFS: DFSSolutionStrategy(),
    SolutionAlgorithm.BFS: BFSSolutionStrategy(),
}


def get_solution_algorithm(name: SolutionAlgorithm) -> MazeSolutionStrategy:
    try:
        return SOLUTION_ALGORITHM_MAP[name]
    except KeyError:
        raise ValueError(
            f"Unknown solver '{name}'. "
            f"Available: {list(SOLUTION_ALGORITHM_MAP)}"
            )


__all__ = [
    "MazeSolutionStrategy",
    "AstarSolutionStrategy",
    "BFSSolutionStrategy",
    "DFSSolutionStrategy",
    "get_solution_algorithm"
]
