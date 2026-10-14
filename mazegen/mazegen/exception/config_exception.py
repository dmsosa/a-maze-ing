class MazeConfigException(Exception):
    """Raised when maze configuration fails."""
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

    def __str__(self) -> str:
        return f"[MazeConfigException] {self.args[0]}"


def raise_mc_error(
                main_msg: str,
                line: int | None = None,
                col: int | None = None
                ) -> None:
    msg = main_msg
    if line:
        msg += f", line: {line}"
    if col:
        msg += f", column: {col}\n"
    raise MazeConfigException(msg)
