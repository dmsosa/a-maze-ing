CORNER_CHARS_SIMPLE = {
    0b0000: " ",
    0b0001: "+", 0b0010: "+", 0b0011: "+",
    0b0100: "+", 0b0101: "+", 0b0110: "+", 0b0111: "+",
    0b1000: "+", 0b1001: "+", 0b1010: "+", 0b1011: "+",
    0b1100: "+", 0b1101: "+", 0b1110: "+", 0b1111: "+",
}


CORNER_CHARS_CLASSIC = {
    0b0000: " ",
    0b0001: "╵", 0b0010: "╶", 0b0011: "└",
    0b0100: "╷", 0b0101: "│", 0b0110: "┌", 0b0111: "├",
    0b1000: "╴", 0b1001: "┘", 0b1010: "─", 0b1011: "┴",
    0b1100: "┐", 0b1101: "┤", 0b1110: "┬", 0b1111: "┼",
}


CORNER_CHARS_CURVED = {
    0b0000: " ",
    0b0001: "╵", 0b0010: "╶", 0b0011: "╰",
    0b0100: "╷", 0b0101: "│", 0b0110: "╭", 0b0111: "├",
    0b1000: "╴", 0b1001: "╯", 0b1010: "─", 0b1011: "┴",
    0b1100: "╮", 0b1101: "┤", 0b1110: "┬", 0b1111: "┼",
}


CORNER_CHARS_DOUBLE = {
    0b0000: " ",
    0b0001: "═", 0b0010: "║", 0b0011: "╚",
    0b0100: "═", 0b0101: "║", 0b0110: "╔", 0b0111: "╠",
    0b1000: "║", 0b1001: "╝", 0b1010: "═", 0b1011: "╩",
    0b1100: "╗", 0b1101: "╣", 0b1110: "╦", 0b1111: "╬",
}


CORNER_CHARS_HEAVY = {
    0b0000: " ",
    0b0001: "━", 0b0010: "┃", 0b0011: "┗",
    0b0100: "━", 0b0101: "┃", 0b0110: "┏", 0b0111: "┠",
    0b1000: "┃", 0b1001: "┛", 0b1010: "━", 0b1011: "┻",
    0b1100: "┓", 0b1101: "┣", 0b1110: "┳", 0b1111: "┿",
}


CORNER_CHARS_BLOCK = {
    0b0000: " ",
    0b0001: "▓", 0b0010: "▓", 0b0011: "▓",
    0b0100: "▓", 0b0101: "▓", 0b0110: "▓", 0b0111: "▓",
    0b1000: "▓", 0b1001: "▓", 0b1010: "▓", 0b1011: "▓",
    0b1100: "▓", 0b1101: "▓", 0b1110: "▓", 0b1111: "▓",
}


CORNER_CHARS_MINIMAL = {
    0b0000: " ",
    0b0001: "·", 0b0010: "·", 0b0011: "·",
    0b0100: "·", 0b0101: "·", 0b0110: "·", 0b0111: "·",
    0b1000: "·", 0b1001: "·", 0b1010: "·", 0b1011: "·",
    0b1100: "·", 0b1101: "·", 0b1110: "·", 0b1111: "·",
}

ThemeChar = dict[str, str | dict[int, str]]

RENDER_THEMES_CHARS: dict[str, ThemeChar] = {
    "simple": {
        "wall_n":  "-",
        "wall_w": "|",
        "space":       " ",
        "corner":    CORNER_CHARS_SIMPLE,
        "current": " @ ",
        "visited": " · ",
        "solution": " ~ ",
        "hunt_pos": " ? ",
        "coin": " © ",
        "blocked":   "█",
        "player":     " @ ",
        "entry":      " S ",
        "exit_":       " E ",
    },
    "classic": {
        "wall_n":  "─",
        "wall_w": "│",
        "space":       " ",
        "corner":    CORNER_CHARS_CLASSIC,
        "current": " @ ",
        "visited": " · ",
        "solution": " ~ ",
        "hunt_pos": " ? ",
        "coin": " © ",
        "blocked":   "█",
        "player":     ":v ",
        "entry":      " S ",
        "exit_":       " E ",
    },
    "curved": {
        "wall_n":   "─",
        "wall_w":   "│",
        "space":    " ",
        "corner": CORNER_CHARS_CURVED,
        "current":  " @ ",
        "visited":  " · ",
        "solution": " ~ ",
        "hunt_pos": " ? ",
        "coin": "🪙",
        "blocked":  "█",
        "player":   "😀",
        "entry":    "🏠",
        "exit_":    "🔑",
    },
    "double": {
        "wall_n":   "═",
        "wall_w":   "║",
        "space":    " ",
        "corner": CORNER_CHARS_DOUBLE,
        "current":  " @ ",
        "visited":  " · ",
        "solution": " ~ ",
        "hunt_pos": " ? ",
        "coin": "🍌",
        "blocked":  "█",
        "player":   "🙉",
        "entry":    "🌿",
        "exit_":    "🪵",
    },
    "heavy": {
        "wall_n":   "━",
        "wall_w":   "┃",
        "space":    " ",
        "corner": CORNER_CHARS_HEAVY,
        "current":  " @ ",
        "visited":  " · ",
        "solution": " ~ ",
        "hunt_pos": " ? ",
        "coin": "🍪",
        "blocked":  "█",
        "player":   "🎃",
        "entry":    "🚪",
        "exit_":    "🪵",
    },
    "block": {
        "wall_n":  "▓",
        "wall_w": "▓",
        "space":       " ",
        "corner":    CORNER_CHARS_BLOCK,
        "current":  " @ ",
        "visited":  " ░ ",
        "solution": " ~ ",
        "hunt_pos": " ? ",
        "coin": "🚬",
        "blocked":   "█",
        "player":     "💀",
        "entry":      "🚪",
        "exit_":       "🥅",
    },
    "minimal": {
        "wall_n":   "·",
        "wall_w":   "|",
        "space":    " ",
        "corner":   CORNER_CHARS_MINIMAL,
        "current":  "O",
        "visited":  ".",
        "solution": "-",
        "hunt_pos": " ? ",
        "coin": "🧀",
        "blocked":  "█",
        "player":   "🐭",
        "entry":    "🚪",
        "exit_":    "🪤",
    },
}


RENDER_THEMES_COLORS: dict[str, dict[str, str]] = {
    "classic": {
        "bg": "#E8C9EB",
        "wall": "#3E3E3E",
        "way": "#ECECEC",
        "current":  "#d58514",
        "visited":   "#6E789D",
        "solution":   "#A1E4AA",
        "hunt_pos": "#ca4700",
        "blocked":    "#457ee9",
    },
    "matrix": {
        "bg": "#000000",
        "wall":       "#00FF1A",
        "current":  "#00f93e",
        "entry":      "#578362",
        "exit_":       "#ffffff",
        "way":        "#101010",
        "blocked":    "#00FF00",
    },
    "sunset": {
        "bg": "#2d1b4e",
        "wall":       "#ff6b35",
        "current":  "#FC9700",
        "entry":      "#ffe574",
        "exit_":       "#ff0000ee",
        "way":        "#98d1e3",
        "blocked":    "#ff9e00",
    },
    "minimal": {
        "bg": "#f8f9fa",
        "wall":       "#212529",
        "current":  "#0d6efd",
        "entry":      "#198754",
        "exit_":       "#dc3545",
        "way":        "#6c757d",
        "blocked":    "#adb5bd",
    },
    "forest": {
        "bg": "#1b2a1b",
        "wall":       "#C94A00",
        "current":  "#f4e285",
        "entry":      "#35D0EB",
        "exit_":       "#029100",
        "way":        "#253426",
        "blocked":    "#2C1500",
    },
    "sepia": {
        "bg":      "#1c1917",
        "wall":    "#a8a29e",
        "current": "#fbbf24",
        "entry":   "#d4a373",
        "exit_":   "#e76f51",
        "way":     "#78716c",
        "blocked": "#ca8a04",
    },
    "sandstone": {
        "bg":      "#292018",
        "wall":    "#c2a878",
        "current": "#f5e6ca",
        "entry":   "#8fbc8f",
        "exit_":   "#cd853f",
        "way":     "#8b7355",
        "blocked": "#daa520",
    },
    # ── pacman ──
    "pacman": {
        "bg":      "#000000",
        "wall":    "#2121ff",
        "current": "#ffff00",
        "entry":   "#00ffff",
        "exit_":   "#ff0000",
        "way":     "#242424",
        "blocked": "#fdbe00",
    },
}


def get_theme_chars(name: str) -> ThemeChar:
    names = set(RENDER_THEMES_CHARS.keys())
    if name not in names:
        raise KeyError(f"Unknown theme '{name}'.Available: {names}")
    return RENDER_THEMES_CHARS[name]


def get_theme_colors(name: str) -> dict[str, str]:
    names = set(RENDER_THEMES_COLORS.keys())
    if name not in names:
        raise KeyError(f"Unknown theme '{name}'. Available: {names}")
    return RENDER_THEMES_COLORS[name]


MOVE_DELTAS: dict[str, tuple[int, int]] = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}
