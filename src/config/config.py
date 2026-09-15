#!/bin/python3
from enum import Enum
from functools import lru_cache
import re
import time
from typing import Any, Optional, Set, Tuple
from config.utils import DEFAULT_COORD, DEFAULT_COORD_STR, random_coord, valid_coord
from constants import KEY_REGEXP, SNAKE_CASE_REGEXP
from exception.config_exception import MazeConfigException
from mazegen import MazeAlgorithm
from pydantic import BaseModel, Field, field_validator, model_validator
from exception import raise_mc_error


class RenderMode(Enum):
    ASCII = "ascii"
    MINILIBX = "mlx"


class MazeConfiguration(BaseModel):
    width: int = Field(default=25, ge=1, le=500)
    height: int = Field(default=25, ge=1, le=500)
    entry: Tuple[int, int] = Field(default=(0,0))
    exit: Tuple[int, int] = Field(default=(0,0))
    algorithm: MazeAlgorithm
    seed: int = 0
    output_file: str = Field(
                            default="output.txt",
                            pattern=SNAKE_CASE_REGEXP
                            )
    config_file: str = Field(
                            default="config_file.txt",
                            pattern=SNAKE_CASE_REGEXP
    )
    perfect: bool
    render_mode: RenderMode = RenderMode.ASCII
    delay: float = Field(default=0.5, ge=0.0, le=30.0)
    pretty: bool = False
    animated: bool = True
    color: bool = False

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    @classmethod
    @lru_cache
    def allowed_keys(cls) -> Set[str]:
        return set(cls.__annotations__.keys())

    @staticmethod
    def parse(raw: str) -> dict[str, Any]:
        """
        Reads configuration file, returns a dictionary.
        Check following errors:
        - Syntax errors
        - key contains not alphanumeric chars
        - key is not included in MazeConfiguration properties
        - key is not uppercase
        Check if keys are missing and informs the user about it


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
            if not key.lower() in config.keys():
                config[key.lower()] = value
            else:
                msg = "" \
                    "\nDuplicated key for MazeConfiguration: " \
                    f"{key} was given more than once (1)." \
                    ""
                raise_mc_error(msg, i + 1, 1)
        # Necessary try convert width and height to integers
        # To be used by parse_coords later.
        MazeConfiguration.check_missing_keys(config)
        try:
            config["width"] = int(config["width"])
            config["height"] = int(config["height"])
            if (config["width"] < 8 or config["height"] < 8):
                print(
                    "[WARNING]: The 42 pattern "
                    "can not be inserted within the maze."
                    )
                time.sleep(1.05)
        except ValueError as e:
            raise_mc_error(
                    f"Error during parsing process: {e}",
                    i
                )
        if isinstance(config["entry"], str):
            config["entry"] = MazeConfiguration.parse_coords(config.get("entry"))
        if isinstance(config["exit"], str):
            config["exit"] = MazeConfiguration.parse_coords(config.get("exit"))
        if not valid_coord(
            config["entry"],
            config["width"],
            config["height"]
            ):
            msg = ""\
                f"Coordinate out of bounds: {config['entry']}" \
                " redirectig to the origin (0,0)." \
                ""
            print(msg)
            config["entry"] = DEFAULT_COORD
            time.sleep(1.05)
        if not valid_coord(
            config["exit"],
            config["width"],
            config["height"]
            ):
            msg = "" \
                f"Coordinate out of bounds: {config['exit']}" \
                " redirectig to a random cell: " \
                ""
            config["exit"] = random_coord(
                    config["width"],
                    config["height"]
                    )
            msg += f"{config['exit']}"
            print(msg)
            time.sleep(1.05)

        if config["entry"] == config["exit"]:
            msg = "" \
                f"entry and exit are equal, redirecting" \
                " the exit to a random coordinate within the maze:" \
                ""
            while config["entry"] == config["exit"]:
                config["exit"] = random_coord(config["width"], config["height"])
            msg += f"{config['exit']}"
            print(msg)
            time.sleep(1.05)
        return config
    
    @staticmethod
    def parse_coords(value: str) -> tuple[int, int]:
        coord = value.split(",")
        if len(coord) != 2:
            msg = "" \
                "Invalid value for coordinates," \
                " must follow the pattern (int, int)" \
                f" received: '{coord}'\n" \
                "using default value: (0, 0)" \
                ""
            print(msg)
            time.sleep(1.05)
            return (0, 0)
        try:
            x = int(coord[0])
            y = int(coord[1])
            return (x, y)
        except ValueError:
            msg = "" \
                "Invalid value for coordinates," \
                "must be integers (int, int)," \
                f" received: '{coord}'" \
                "using default value: (0, 0)" \
                ""
            print(msg)
            time.sleep(1.05)
            return (0, 0)               


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
            if not re.match(KEY_REGEXP, letter):
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

    @staticmethod
    def check_missing_keys(config_dict: dict[str, str]) -> None:
        model_fields = MazeConfiguration.model_fields


        for name, field in model_fields.items():
            if name not in config_dict:
                config_dict[name] = field.default
                print(
                    f"Option '{name}' not found, \
using default: {field.default}"
                    )
                time.sleep(1.05)

    @staticmethod
    @lru_cache
    def default_config() -> "MazeConfiguration":
        return MazeConfiguration(
            width=25,
            height=25,
            entry=(0, 0),
            exit=(24, 24),
            algorithm=MazeAlgorithm.HUNT_AND_KILL,
            seed=3,
            output_file="maze_output.txt",
            perfect=False,
            render_mode=RenderMode.ASCII,
        )
    