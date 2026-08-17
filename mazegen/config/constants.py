import re

from ..model.maze import MazeAlgorithm


SNAKE_CASE_REGEXP = re.compile(r"^[a-z0-9]+(?:_[a-zA-Z0-9]+)*\.txt$")


DEFAULT_CONFIG: dict[str, str | None] = {
    "WIDTH": None,
    "HEIGHT": None,
    "ENTRY": None,
    "EXIT": None,
    "SEED": 3,
    "OUTPUT_FILE": "maze_output.txt",
    "PERFECT": False,
    "DISPLAY_MODE": "ASCII",
    "ALGORITHM": "DFS",
}


CONFIG_KEYS = [
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "SEED",
    "OUTPUT_FILE",
    "PERFECT",
    "DISPLAY_MODE",
    "ALGORITHM",
]

VALID_ALGO = [algo.value for algo in MazeAlgorithm]


REQUIRED_CONFIG_KEYS = [
    "WIDTH",
    "HEIGHT"
]
