class MazeException(Exception):
    """Raised when maze generation fails."""
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

    def __str__(self) -> str:
        return f"[MazeException] {self.args[0]}"

    @staticmethod
    def out_of_bounds_msg(x: int, y: int, width: int, height: int) -> str:
        msg = "" \
            "Coordinates out of bounds, must be between" \
            " the values for widht and height: " \
            f"'(0 <= x < {width})' and " \
            f"'(0 <= y < {height})', " \
            f"but received ({x}, {y})" \
            ""
        return msg
