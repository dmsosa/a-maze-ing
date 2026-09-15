from enum import Enum


class MazeAlgorithm(Enum):
    """Generation options, algorithm types"""
    DFS = "DFS"
    HUNT_AND_KILL = "HUNT_AND_KILL"
    PRIM = "PRIM"
