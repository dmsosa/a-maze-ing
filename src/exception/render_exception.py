from functools import lru_cache
import os
import sys


class RenderError(Exception):
    """Raised when the renderer cannot draw to the current output stream."""
