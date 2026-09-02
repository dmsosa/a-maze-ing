
from mazegen.algorithm.base import MazeAlgorithmStrategy
from mazegen.algorithm.huntkill import HuntKillAlgorithm
from mazegen.model.constants import MazeAlgorithm


ALGORITHM_MAP: dict[MazeAlgorithm, MazeAlgorithmStrategy] = {
    MazeAlgorithm.HUNT_N_KILL: HuntKillAlgorithm(),
    MazeAlgorithm.DFS: HuntKillAlgorithm(),
}


def get_algorithm(name: MazeAlgorithm) -> MazeAlgorithmStrategy:
    try:
        return ALGORITHM_MAP[name]
    except KeyError:
        raise ValueError(f"Algorithm for name '{name}' not implemented")
