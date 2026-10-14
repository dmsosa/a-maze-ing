import re

from pydantic import ValidationError
from ..exception import MazeConfigException

SNAKE_CASE_REGEXP = re.compile(r"^[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*\.txt$")
KEY_REGEXP = re.compile(r'^[A-Za-z_-]+$')

TITLE = "Welcome to the A-Maze-Ing project...\n"
SUBTITLE = "Enjoy, and find your way ;)."
MAIN_INSTRUCTION = "Type 'quit' to exit, Ctrl+C to interrupt, Ctrl+D for EOF."

# ERRORS

ERROR_MAP = {
    FileNotFoundError: "The file '{file}' does not exist.",
    PermissionError:   "Permission denied to read '{file}'.",
    MazeConfigException: "{e}",
    ValidationError: "{e}",
}
