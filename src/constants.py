import re
from typing import KeysView

from mazegen import MazeAlgorithm, MazeGenerator


SNAKE_CASE_REGEXP = re.compile(r"^[a-z0-9]+(?:_[a-zA-Z0-9]+)*\.txt$")


DEFAULT_CONFIG: dict[str, str | None | int] = {
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


ALLOWED_PROPS = KeysView[str] = MazeGenerator.__dict__.keys()

VALID_ALGO = [algo.value for algo in MazeAlgorithm]


REQUIRED_CONFIG_KEYS = [
    "WIDTH",
    "HEIGHT"
]
