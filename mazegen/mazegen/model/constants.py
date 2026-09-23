from enum import Enum
import re


class MazeAlgorithm(Enum):
    """Generation options, algorithm types"""
    DFS = "DFS"
    HUNT_AND_KILL = "HUNT_AND_KILL"
    PRIM = "PRIM"


class SolutionAlgorithm(Enum):
    """Generation options, algorithm types"""
    DFS = "dfs"
    ASTAR = "astar"
    BFS = "bfs"


SNAKE_CASE_REGEXP = re.compile(r"^[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*\.txt$")


KEY_REGEXP = re.compile(r'^[A-Za-z_-]+$')
