#!/bin/python3


from typing import KeysView, List, Tuple

from constants import REQUIRED_CONFIG_KEYS
from mazegen import MazeGenerator


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
    allowed_props: KeysView[str] = MazeGenerator.__dict__.keys()
    for i, letter in enumerate(key):
        if not letter.isalpha():
            msg = "" \
                "Invalid key, contains non alphabetic character: " \
                ", must one of the following: " \
                f"{allowed_props}" \
                ""
            return (msg, int(i))
        if not (key in allowed_props):
            msg = "" \
                "Invalid key, " \
                ", must one of the following: " \
                f"{allowed_props}" \
                ""
            return (msg, 1)
        if not (key in allowed_props):
            msg = "" \
                "Invalid key, " \
                "key must be uppercase: " \
                f"{key}" \
                ""
            return (msg, 1)
    return (None, None)


def validate_config(config: dict[str, str]) -> List[str]:
    """
    Verifies that config dictionary contains the mandatory keys
    see (REQUIRED_CONFIG_KEYS), it does not validate the values.
    The purpose of this function is to check that it
    has the required keys to build our maze later

    :return: List of error messages for missing keys,
    empty list if no missing keys
    :rtype: List[str]
    """

    missing = [
        k for k in config.keys()
        if not (k in REQUIRED_CONFIG_KEYS)
        ]
    return missing
