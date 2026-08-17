from pydantic import BaseModel
from .constants import CONFIG_KEYS, DEFAULT_CONFIG, REQUIRED_CONFIG_KEYS, SNAKE_CASE_REGEXP, VALID_ALGO
from ..exception import raise_mc_error


def check_missing_config(config: dict[str, str]) -> dict[str, str]:
    missing = [k for k in REQUIRED_CONFIG_KEYS if not config.get(k)]
    if len(missing) > 0:
        msg = "\nConfig error, required Maze Options:\n"
        for m in missing:
            m += f" - '{m}'\n"
        raise_mc_error(msg)
    return config


def check_config_received(config: dict[str, str]) -> dict[str, str]:
        for k, v in config.items():
            try:
                if not v:
                    raise ValueError(f"Value must not be NULL: {k}")
                if (k in ["WIDTH", "HEIGHT", "SEED"]):
                    config[k] = int(v)
                elif (k in ["ENTRY", "EXIT"]):
                    parts = v.split(",")
                    if (len(parts) != 2):
                        raise ValueError(f"tuple for ENTRY and EXIT must meet the format: (int, int), passed {parts}")
                    config[k] = tuple([int(parts[0]), int(parts[1])])
                elif (k in ["OUTPUT_FILE"]):
                    match = SNAKE_CASE_REGEXP.search(v)
                    if not match:
                        msg = "Output file must be written in snake_Case and have .txt extention:"
                        msg += f"\nreceived: {v}\nexample: maze_output.txt"
                        raise ValueError(msg)
                    config[k] = v
                elif (k in ["PERFECT"]):
                    val = v.lower()
                    if (val != "true" and val != "false"):
                        raise ValueError(f"Not valid boolean value: {v}")
                elif (k in ["ALGORITHM"]):
                    val = v.upper()
                    if val not in VALID_ALGO:
                        msg = f"Not valid algorithm value: {v}\n"
                        msg += f"valid values: {VALID_ALGO}"
                        raise ValueError(msg)
            except ValueError as e:
                msg = f"\nError while validating configuration for Maze key:'{k}':\n"
                msg += e.__str__()
                raise_mc_error(msg)
        return config


def set_default_values(config: dict[str, str]) -> dict[str, str]:
    missing = [k for k in CONFIG_KEYS if not config.get(k)]
    if len(missing) > 0:
        for m in missing:
            value = DEFAULT_CONFIG.get(m)
            msg = f"\nNot received maze option: '{m}'\n"
            msg += f"Using default value: '{value}'\n"
            print(msg)
            config[m] = value
    return config


def validate_config(config: dict[str, str]) -> dict[str, str]:
    config = check_config_received(config)
    config = check_missing_config(config)
    config = set_default_values(config)
    return config

class MazeConfiguration(BaseModel):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def parse(raw: str) -> None:
        lines: list[str] = raw.split('\n')
        lines_len: int = len(lines)
        nl_count: int = 0
        config: dict[str, str | None] = {}
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
            if not line[0].isalpha():
                msg = "\nEvery line must start with alphabetic characters"
                raise_mc_error(msg, i+1)
            parts = line.split("=")
            if (len(parts) != 2):
                msg = "Bad configuration syntax, follow the rules: "
                msg += "'KEY=VALUE'"
                raise_mc_error(msg, i + 1, len(parts[-1]))
            key, value = parts
            if key != key.upper():
                msg = "Bad configuration syntax, key must be uppercase: "
                msg += "'KEY=VALUE'"
                raise_mc_error(msg, i + 1, len(key))
            if key not in CONFIG_KEYS:
                msg = "Unknown Maze Key, key must be one of: "
                msg += f"{CONFIG_KEYS}"
                raise_mc_error(msg, i + 1, len(key))
            if len(value) < 1:
                msg = f"Bad Maze Value, must not be NULL: {key}"
                raise_mc_error(msg, i + 1, len(key))
            config[key] = value
        return validate_config(config)
