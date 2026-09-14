CORNER_CHARS = {
    0b0000: " ",
    0b0001: "╵", 0b0010: "╶", 0b0011: "└",
    0b0100: "╷", 0b0101: "│", 0b0110: "┌", 0b0111: "├",
    0b1000: "╴", 0b1001: "┘", 0b1010: "─", 0b1011: "┴",
    0b1100: "┐", 0b1101: "┤", 0b1110: "┬", 0b1111: "┼",
}


WALL_BIT = {"N": 0x1, "E": 0x2, "S": 0x4, "W": 0x8}


def has_wall(hex_char: str, direction: str) -> bool:
    """Decode a single hex digit (WSEN bit layout) without touching Cell/Direction."""
    return bool(int(hex_char, 16) & WALL_BIT[direction])


def wall_go_to(digits, cx, cy, width, height, direction) -> bool:
    """
    The goal with the corners is to check:
    if this is the first row, first col, put the left corner
    :param: digits where I get the hexadecimal digits
    :param: x, y the coordinates of the maze(digits) I am working on
    :param: width, height, to check if I am in the last row or col
    :param: direction, to check one direction

    Is there a wall-line touching corner (cx, cy) going `direction`?
    """
    if direction == "N":
        if cy == 0:
            return False
        return has_wall(digits[cy - 1][cx], "W") if cx < width \
            else has_wall(digits[cy - 1][cx - 1], "E")
    if direction == "S":
        if cy == height:
            return False
        return has_wall(digits[cy][cx], "W") if cx < width \
            else has_wall(digits[cy][cx - 1], "E")
    if direction == "W":
        if cx == 0:
            return False
        return has_wall(digits[cy][cx - 1], "N") if cy < height \
            else has_wall(digits[cy - 1][cx - 1], "S")
    if direction == "E":
        if cx == width:
            return False
        return has_wall(digits[cy][cx], "N") if cy < height \
            else has_wall(digits[cy - 1][cx], "S")
    raise ValueError(direction)