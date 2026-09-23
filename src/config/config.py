#!/bin/python3
from enum import Enum
from functools import lru_cache
import re
import sys
from typing import Any, Set, Tuple
from config.utils import DEFAULT_COORD, print_sleep, random_coord, valid_coord
from constants import KEY_REGEXP, SNAKE_CASE_REGEXP
from mazegen import MazeAlgorithm, SolutionAlgorithm
from pydantic import BaseModel, Field, model_validator
from exception import raise_mc_error


class RenderMode(Enum):
    ASCII = "ascii"
    MINILIBX = "mlx"


class MazeConfiguration(BaseModel):
    width: int = Field(default=25, ge=1, le=500)
    height: int = Field(default=25, ge=1, le=500)
    entry: Tuple[int, int] = Field(default=(0, 0))
    exit: Tuple[int, int] = Field(default=(0, 0))
    algorithm: MazeAlgorithm = MazeAlgorithm.PRIM
    solution_algorithm: SolutionAlgorithm = SolutionAlgorithm.ASTAR
    seed: int = Field(default=0, ge=0)
    output_file: str = Field(
                            default="output.txt",
                            pattern=SNAKE_CASE_REGEXP
                            )
    config_file: str = Field(
                            default="config_file.txt",
                            pattern=SNAKE_CASE_REGEXP
    )
    perfect: bool = True
    render_mode: RenderMode = RenderMode.ASCII
    delay: float = Field(default=0.025, ge=0.0, le=30.0)
    pretty: bool = False
    animated: bool = True
    color: bool = False
    cell_size: int = 3

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def update_config(self, name: str, value: Any) -> "MazeConfiguration":
        data = self.model_dump()
        data.update(**{name: value})
        return MazeConfiguration(**data)

    @model_validator(mode="after")
    def post_validation_coords(self) -> "MazeConfiguration":
        if not valid_coord(self.entry, self.width, self.height):
            msg = "" \
                "After validation method found " \
                "invalid coordinate for entry: " \
                f"({self.entry}), " \
                "redirected to the origin (0, 0)" \
                ""
            print(msg, file=sys.stderr)
            self.entry = (0, 0)
        if not valid_coord(self.exit, self.width, self.height):
            msg = "" \
                "After validation method found " \
                "invalid coordinate for exit: " \
                f"{self.exit}, " \
                "redirected to bot-right corner " \
                f"({self.width - 1}, {self.height - 1})" \
                ""
            print(msg, file=sys.stderr)
            self.exit = (self.width - 1, self.height - 1)
        if self.entry == self.exit:
            msg = "" \
                "After validation method found " \
                "that exit and entry are equal: " \
                f"({self.entry}), " \
                "redirected exit to bot-right corner: " \
                f"({self.width - 1}, {self.height - 1})" \
                ""
            print(msg, file=sys.stderr)
            self.exit = (self.width - 1, self.height - 1)
        return self

    def redirect_entries(self) -> None:
        self.entry = (0, 0)
        self.exit = (self.width - 1, self.height - 1)
        msg = "" \
            "Manually redirecting entry and exit" \
            " to the origin and bot-right corner " \
            f"respectively: (0, 0) and ({self.width - 1}, {self.height - 1})" \
            ""
        print(msg, file=sys.stderr)

    @classmethod
    @lru_cache
    def allowed_keys(cls) -> Set[str]:
        return set(cls.__annotations__.keys())

    @staticmethod
    def parse(raw: str, verbose: bool = False, debug=True) -> dict[str, Any]:
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
        MazeConfiguration.check_missing_keys(config, verbose)
        try:
            config["width"] = int(config["width"])
            config["height"] = int(config["height"])
            if (config["width"] < 8 or config["height"] < 8):
                msg = "" \
                      "[WARNING]: The 42 pattern " \
                      "can not be inserted within the maze." \
                      ""
                if verbose:
                    print_sleep(msg)
                if debug:
                    print(msg, file=sys.stderr)
        except ValueError as e:
            raise_mc_error(
                    f"Error during parsing process: {e}",
                    i
                )
        if isinstance(config["entry"], str):
            config["entry"] = MazeConfiguration.parse_coords(
                config.get("entry"),
                verbose
            )
        if isinstance(config["exit"], str):
            config["exit"] = MazeConfiguration.parse_coords(
                config.get("exit"),
                verbose
                )
        if not valid_coord(
            config["entry"],
            config["width"],
            config["height"]
        ):
            msg = ""\
                f"Coordinate out of bounds: {config['entry']}" \
                " redirectig to the origin (0,0)." \
                ""
            config["entry"] = DEFAULT_COORD
            if verbose:
                print_sleep(msg)
            if debug:
                print(msg, file=sys.stderr)
        if not valid_coord(
            config["exit"],
            config["width"],
            config["height"]
        ):
            msg = "" \
                f"Coordinate out of bounds: {config['exit']}" \
                " redirectig to the bottom and right-most cell: " \
                ""
            config["exit"] = (
                config["width"] - 1,
                config["height"] - 1
            )
            msg += f"{config['exit']}"
            if verbose:
                print_sleep(msg)
            if debug:
                print(msg, file=sys.stderr)
        if config["entry"] == config["exit"]:
            msg = "" \
                "entry and exit are equal, redirecting" \
                " the exit to a random coordinate within the maze:" \
                ""
            while config["entry"] == config["exit"]:
                config["exit"] = random_coord(
                    config["width"],
                    config["height"]
                    )
            msg += f"{config['exit']}"
            if verbose:
                print_sleep(msg)
            if debug:
                print(msg, file=sys.stderr)
        if debug:
            print(
                f"config dict parsed successfully: {config}", file=sys.stderr
            )
        return config

    @staticmethod
    def parse_coords(value: str, verbose: bool = False, debug=True
                     ) -> tuple[int, int]:
        coord = value.split(",")
        if len(coord) != 2:
            msg = "" \
                "Invalid value for coordinates," \
                " must follow the pattern (int, int)" \
                f" received: '{coord}'\n" \
                "using default value: (0, 0)" \
                ""
            if verbose:
                print_sleep(msg)
            if debug:
                print(msg, file=sys.stderr)
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
            if verbose:
                print_sleep(msg)
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
    def check_missing_keys(
        config_dict: dict[str, str],
        verbose: bool = False,
        debug: bool = True
    ) -> None:
        model_fields = MazeConfiguration.model_fields

        for name, field in model_fields.items():
            if name not in config_dict:
                config_dict[name] = field.default
                msg = f"Option '{name}'not found," \
                      f"using default: {field.default}"
                if verbose:
                    print_sleep(msg)
                if debug:
                    print(msg, file=sys.stderr)

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
