import re

from pydantic import ValidationError
from exception.config_exception import MazeConfigException

SNAKE_CASE_REGEXP = re.compile(r"^[a-z0-9]+(?:_[a-zA-Z0-9]+)*\.txt$")
KEY_REGEXP = re.compile(r'^[A-Za-z_-]+$')

# ERRORS

ERROR_MAP = {
    FileNotFoundError: "The file '{file}' does not exist.",
    PermissionError:   "Permission denied to read '{file}'.",
    MazeConfigException: "{e}",
    ValidationError: "{e}",
}
