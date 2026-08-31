from typing import KeysView

from .validation import validate_key
from mazegen import MazeGenerator
from exception import raise_mc_error


class MazeConfiguration():
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def parse(raw: str) -> dict[str, str]:
        """
        Reads configuration file and check following errors:
        - Syntax errors
        - key contains not alphanumeric chars
        - key is not included in MazeGenerator properties
        - key is not uppercase
        See .mazegen.constants.py.




        :param str filename: The path to the config file to be read
        :return: Returns dictionary with keys and values, note that
        values are not checked
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
                    "Bad configuration syntax, follow the rules: " \
                    "'KEY=VALUE'" \
                    ""
                raise_mc_error(msg, i + 1, 1)
            key, value = parts
            error_msg, index_error = validate_key(key)
            if error_msg:
                allowed_props: KeysView[str] = MazeGenerator.__dict__.keys()
                msg = "" \
                    "Invalid key, must one of the following: " \
                    f"{allowed_props}" \
                    ""
                raise_mc_error(msg, i+1, index_error)
            if len(value) < 1:
                msg = f"Bad Maze Value, must not be NULL: {key}"
                raise_mc_error(msg, i + 1, len(key))
            config[key] = value

        return config
