
from mazegen.algorithm.base import MazeAlgorithmStrategy
from mazegen.algorithm.huntkill import HuntKillAlgorithm
from mazegen.algorithm.recursive_backtracker import RecursiveBacktrackerAlgorithm
from mazegen.algorithm.prim import PrimAlgorithm
from mazegen.model.constants import MazeAlgorithm


ALGORITHM_MAP: dict[MazeAlgorithm, MazeAlgorithmStrategy] = {
    MazeAlgorithm.HUNT_AND_KILL: HuntKillAlgorithm(),
    MazeAlgorithm.DFS: RecursiveBacktrackerAlgorithm(),
    MazeAlgorithm.PRIM: PrimAlgorithm(),
}


def get_algorithm(name: MazeAlgorithmStrategy) -> MazeAlgorithmStrategy:
    try:
        return ALGORITHM_MAP[name]
    except KeyError:
        raise ValueError(f"Algorithm for name '{name}' not implemented")
