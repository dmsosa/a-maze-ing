class MazeConfigException(Exception):
    """Raised when maze configuration fails."""
    def __init__(self, msg: str):
        super().__init__(msg)

    def __str__(self):
        return f"[MazeConfigException] {self.args[0]}"


def raise_mc_error(
            main_msg: str,
            line: int | None = None,
            col: int | None = None
            ) -> None:
            msg = ""
            if line:
                msg += f"line: {line}"
            if col:
                msg += f", column: {col}\n"
            msg += main_msg
            raise MazeConfigException(msg)
