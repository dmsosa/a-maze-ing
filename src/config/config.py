#!/bin/python3
from enum import Enum
from typing import Any, List, Optional, Set, Tuple
from mazegen import MazeAlgorithm
from pydantic import BaseModel, Field, field_validator, model_validator
from exception import raise_mc_error


class RenderMode(Enum):
    ASCII = "ascii"
    OTHER = "other"


class MazeConfiguration(BaseModel):
    width: int = Field(..., ge=8, le=120)
    height: int = Field(..., ge=8, le=120)
    entry: Optional[Tuple[int, int]] = None
    exit: Optional[Tuple[int, int]] = None
    algorithm: MazeAlgorithm
    seed: int
    output_file: str = Field(
                            default="output.txt",
                            pattern=r"^[a-zA-Z0-9]\.txt$"
                            )
    perfect: bool
    render_mode: RenderMode = RenderMode.ASCII

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    @field_validator("entry", "exit", mode="before")
    @classmethod
    def validate_coords(cls, value: Any) -> Any:
        if isinstance(value, str):
            coord = value.split(",")
            if len(coord) != 2:
                msg = "" \
                    "Invalid value for coordinates," \
                    " must follow the pattern (int, int)" \
                    f" received: '{coord}'" \
                    ""
                raise ValueError(msg)
            try:
                x = int(coord[0].strip())
                y = int(coord[1].strip())
                return (x, y)
            except ValueError:
                msg = "" \
                    "Invalid value for coordinates," \
                    "must be integers (int, int)," \
                    f" received: '{coord}'" \
                    ""
                raise ValueError(msg)
        return value

    @classmethod
    def allowed_keys(cls) -> Set[str]:
        return set(cls.__annotations__.keys())

    @staticmethod
    def parse(raw: str) -> dict[str, Any]:
        """
        Reads configuration file and check following errors:
        - Syntax errors
        - key contains not alphanumeric chars
        - key is not included in MazeConfiguration properties
        - key is not uppercase

        :param str raw: Config file's content to be read (just raw bytes)
        :return: Returns dictionary with keys and values,
        values are not validated
        :rtype: dict[str, str]
        :raises: MazeConfigurationError, if some of the errors
        is found, it raises the first error that is found
        """
        lines: list[str] = raw.split('\n')
        lines_len: int = len(lines)
        nl_count: int = 0
        config: dict[str, str] = {}
        for i in range(0, lines_len):
            line = lines[i]
            if nl_count > 1:
                msg = "\nFound two (2) consecutive new lines"
                raise_mc_error(msg, i)
            if len(line) == 0:
                nl_count += 1
                continue
            else:
                nl_count = 0
            if line[0] == "#":
                continue
            parts = line.split("=")
            if (len(parts) != 2):
                msg = "" \
                    "Bad configuration syntax," \
                    "follow the rules: " \
                    "'KEY=VALUE'" \
                    ""
                raise_mc_error(msg, i + 1, 1)
            key, value = parts
            error_msg, index_error = MazeConfiguration.validate_key(key)
            if error_msg:
                raise_mc_error(error_msg, i+1, index_error)
            config[key.lower()] = value
        return config

    @staticmethod
    def validate_key(key: str) -> Tuple[str | None, int | None]:
        """
        Check if key is included in VALID KEYS constant.
        See .mazegen.config.constants.py.
        Returns error if:
        - key contains not alphanumeric chars
        - key is not included in CONFIG_KEYS
        - key is not uppercase

        :param str key: The string to be validated
        :return: Tuple with error message if invalid,
        otherwise empty string if valid, and
        index of first invalid letter
        :rtype: Tuple[bool, int | None]
        """
        allowed_keys = [
            key.upper()
            for key in MazeConfiguration.allowed_keys()
            ]
        for i, letter in enumerate(key):
            if not letter.isalpha():
                msg = "" \
                    f"Invalid key '{key}'," \
                    " contains non alphabetic character," \
                    f" must one of the following: {allowed_keys}" \
                    ""
                return (msg, int(i))
            if key != key.upper():
                msg = "" \
                    "Invalid key, " \
                    " must be written in uppercase: " \
                    f"{key}" \
                    ""
                return (msg, 1)
            if not (key.upper() in allowed_keys):
                msg = "" \
                    "Invalid key, " \
                    ", must one of the following: " \
                    f"{allowed_keys}" \
                    ""
                return (msg, 1)

        return (None, None)

    @model_validator(mode="after")
    def validate_config(self) -> "MazeConfiguration":
        for name, coord in (
                    ("entry", self.entry),
                    ("exit", self.exit)
                ):
            if coord is not None:
                x, y = coord
                if not (0 <= x < self.width):
                    msg = "" \
                        f"{name} has coordinates out of bounds," \
                        f" received (>>{x}<<,{y}) (width={self.width})" \
                        ""
                    raise ValueError(msg)
                if not (0 <= y < self.height):
                    msg = "" \
                        f"{name} has coordinates out of bounds," \
                        f" received ({x},>>{y}<<) (height={self.height})" \
                        ""
                    raise ValueError(msg)
            elif name == "exit":
                self.exit = (self.width - 1, self.height - 1)
            else:
                self.entry = (0, 0)
        return self


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


VALID_ALGO:  List[str] = [algo.value for algo in MazeAlgorithm]


REQUIRED_CONFIG_KEYS = [
    "WIDTH",
    "HEIGHT"
]


COORD_KEYS = [
    "ENTRY",
    "EXIT"
]
