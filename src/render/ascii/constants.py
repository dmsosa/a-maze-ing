from render.ascii.grid import CORNER_CHARS


CELL_WIDTH = 3


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


CORNER_CHARS_HEAVY =  {
    0b0000: " ",
    0b0001: "━", 0b0010: "┃", 0b0011: "┗",
    0b0100: "━", 0b0101: "┃", 0b0110: "┏", 0b0111: "┠",
    0b1000: "┃", 0b1001: "┛", 0b1010: "━", 0b1011: "┻",
    0b1100: "┓", 0b1101: "┣", 0b1110: "┳", 0b1111: "┿",
}


CORNER_CHARS_DASHED =  {
    0b0000: " ",
    0b0001: "▀", 0b0010: "▌", 0b0011: "▀",
    0b0100: "▄", 0b0101: "▌", 0b0110: "▄", 0b0111: "▌",
    0b1000: "▐", 0b1001: "▀", 0b1010: "▄", 0b1011: "▀",
    0b1100: "▄", 0b1101: "▌", 0b1110: "▄", 0b1111: "█",
},


CORNER_CHARS_SHADOW =  {
    0b0000: " ",
    0b0001: "▀", 0b0010: "▌", 0b0011: "▀",
    0b0100: "▄", 0b0101: "▌", 0b0110: "▄", 0b0111: "▌",
    0b1000: "▐", 0b1001: "▀", 0b1010: "▄", 0b1011: "▀",
    0b1100: "▄", 0b1101: "▌", 0b1110: "▄", 0b1111: "█",
},


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


RENDER_THEMES_CHARS: dict[str, dict[str, str]] = {
    "simple": {
        "wall_n":  "-"*CELL_WIDTH,
        "wall_w": "|",
        "space":       " "*CELL_WIDTH,
        "corner":    CORNER_CHARS_SIMPLE,
        "current": "@".center(CELL_WIDTH, " "),
        "visited": "·".center(CELL_WIDTH, " "),
        "solution": "~".center(CELL_WIDTH, " "),
        "hunt_pos": "?".center(CELL_WIDTH, " "),
        "blocked":   "█"*CELL_WIDTH,
        "player":     "🚶🏻‍➡️".center(CELL_WIDTH, " "),
        "entry":      "🚪".center(CELL_WIDTH, " "),
        "exit_":       "🔑".center(CELL_WIDTH, " "),
    },
    "classic": {
        "wall_n":  "─"*CELL_WIDTH,
        "wall_w": "│",
        "space":       " "*CELL_WIDTH,
        "corner":    CORNER_CHARS_CLASSIC,
        "current": "@".center(CELL_WIDTH, " "),
        "visited": "·".center(CELL_WIDTH, " "),
        "solution": "~".center(CELL_WIDTH, " "),
        "hunt_pos": "?".center(CELL_WIDTH, " "),
        "blocked":   "█"*CELL_WIDTH,
        "player":     "🚶🏻‍➡️".center(CELL_WIDTH, " "),
        "entry":      "🚪".center(CELL_WIDTH, " "),
        "exit_":       "🔑".center(CELL_WIDTH, " "),
    },
    "curved": {
        "wall_n":   "─" * CELL_WIDTH,
        "wall_w":   "│",
        "space":    " " * CELL_WIDTH,
        "corner": CORNER_CHARS_CURVED,
        "current":  "@".center(CELL_WIDTH, " "),
        "visited":  "·".center(CELL_WIDTH, " "),
        "solution": "~".center(CELL_WIDTH, " "),
        "hunt_pos": "?".center(CELL_WIDTH, " "),
        "blocked":  "█" * CELL_WIDTH,
        "player":   "🚶🏻‍➡️".center(CELL_WIDTH, " "),
        "entry":    "🚪".center(CELL_WIDTH, " "),
        "exit_":    "🔑".center(CELL_WIDTH, " "),
    },
    "double": {
        "wall_n":   "═" * CELL_WIDTH,
        "wall_w":   "║",
        "space":    " " * CELL_WIDTH,
        "corner": CORNER_CHARS_DOUBLE,
        "current":  "@".center(CELL_WIDTH, " "),
        "visited":  "·".center(CELL_WIDTH, " "),
        "solution": "~".center(CELL_WIDTH, " "),
        "hunt_pos": "?".center(CELL_WIDTH, " "),
        "blocked":  "█" * CELL_WIDTH,
        "player":   "🚶🏻‍➡️".center(CELL_WIDTH, " "),
        "entry":    "🚪".center(CELL_WIDTH, " "),
        "exit_":    "🔑".center(CELL_WIDTH, " "),
    },
    "heavy": {
        "wall_n":   "━" * CELL_WIDTH,
        "wall_w":   "┃",
        "space":    " " * CELL_WIDTH,
        "corner": CORNER_CHARS_HEAVY,
        "current":  "@".center(CELL_WIDTH, " "),
        "visited":  "·".center(CELL_WIDTH, " "),
        "solution": "~".center(CELL_WIDTH, " "),
        "hunt_pos": "?".center(CELL_WIDTH, " "),
        "blocked":  "█" * CELL_WIDTH,
        "player":   "🚶🏻‍➡️".center(CELL_WIDTH, " "),
        "entry":    "🚪".center(CELL_WIDTH, " "),
        "exit_":    "🔑".center(CELL_WIDTH, " "),
    },
    "dashed": {
        "wall_n":   "╌" * CELL_WIDTH,
        "wall_w":   "╎",
        "space":    " " * CELL_WIDTH,
        "corner": CORNER_CHARS_DASHED,
        "current":  "@".center(CELL_WIDTH, " "),
        "visited":  "·".center(CELL_WIDTH, " "),
        "solution": "~".center(CELL_WIDTH, " "),
        "hunt_pos": "?".center(CELL_WIDTH, " "),
        "blocked":  "█" * CELL_WIDTH,
        "player":   "🚶🏻‍➡️".center(CELL_WIDTH, " "),
        "entry":    "🚪".center(CELL_WIDTH, " "),
        "exit_":    "🔑".center(CELL_WIDTH, " "),
    },
    "shadow": {
        "wall_n":   "▄" * CELL_WIDTH,
        "wall_w":   "▐",
        "space":    " " * CELL_WIDTH,
        "corner": CORNER_CHARS_SHADOW,
        "current":  "@".center(CELL_WIDTH, " "),
        "visited":  "·".center(CELL_WIDTH, " "),
        "solution": "~".center(CELL_WIDTH, " "),
        "hunt_pos": "?".center(CELL_WIDTH, " "),
        "blocked":  "█" * CELL_WIDTH,
        "player":   "🚶🏻‍➡️".center(CELL_WIDTH, " "),
        "entry":    "🚪".center(CELL_WIDTH, " "),
        "exit_":    "🔑".center(CELL_WIDTH, " "),
    },
    "block": {
        "wall_n":  "▓"*CELL_WIDTH,
        "wall_w": "▓",
        "way":       "░",
        "space":       " "*CELL_WIDTH,
        "corner":    CORNER_CHARS_BLOCK,
        "blocked":   "█"*CELL_WIDTH,
        "player":     "🚶🏻‍➡️",
        "entry":      "🚪",
        "exit_":       "🔑",
    },
    "minimal": {
        "wall_n":   "·" * CELL_WIDTH,
        "wall_w":   "·",
        "space":    " " * CELL_WIDTH,
        "corner":   CORNER_CHARS_MINIMAL,
        "current":  "O".center(CELL_WIDTH, " "),
        "visited":  ".".center(CELL_WIDTH, " "),
        "solution": "-".center(CELL_WIDTH, " "),
        "hunt_pos": "?".center(CELL_WIDTH, " "),
        "blocked":  "█" * CELL_WIDTH,
        "player":   "🚶🏻‍➡️".center(CELL_WIDTH, " "),
        "entry":    "🚪".center(CELL_WIDTH, " "),
        "exit_":    "🔑".center(CELL_WIDTH, " "),
    },
}



RENDER_THEMES_COLORS: dict[str, dict[str, str]] = {
    "classic": {
        "bg": "#E8C9EB",
        "wall": "#787878",
        "way": "#CECECE",
        "current":  "#d58514",
        "visited":   "#38247E",
        "solution":   "#A1E4AA",
        "hunt_pos": "#ca4700",
        "blocked":    "#e94560",
    },
    "matrix": {
        "bg": "#000000",
        "wall":       "#003300",
        "current":  "#00ff41",
        "entry":      "#00cc33",
        "exit_":       "#ffffff",
        "way":        "#008822",
        "blocked":    "#005500",
    },
    "ocean": {
        "bg": "#0a1628",
        "wall":       "#1e90ff",
        "current":  "#ffd700",
        "entry":      "#40e0d0",
        "exit_":       "#ff6347",
        "way":        "#4682b4",
        "blocked":    "#00bfff",
    },
    "sunset": {
        "bg": "#2d1b4e",
        "wall":       "#ff6b35",
        "current":  "#ffd93d",
        "entry":      "#6bcb77",
        "exit_":       "#ff477e",
        "way":        "#c77dff",
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
        "wall":       "#4a7c59",
        "current":  "#f4e285",
        "entry":      "#998004",
        "exit_":       "#d4a373",
        "way":        "#52796f",
        "blocked":    "#355e3b",
    },
    "ice": {
        "bg": "#0b132b",
        "wall":       "#3a506b",
        "current":  "#dff9fb",
        "entry":      "#a3cef1",
        "exit_":       "#ff595e",
        "way":        "#5bc0be",
        "blocked":    "#1b262c",
    },
    "pastel": {
        "bg":      "#faf5ff",
        "wall":    "#c4b5fd",
        "current": "#f9a8d4",
        "entry":   "#86efac",
        "exit_":   "#fca5a5",
        "way":     "#a5b4fc",
        "blocked": "#fcd34d",
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
        "way":     "#ffb8ae",
        "blocked": "#ff00ff",
    },
}


def get_theme_chars(name: str) -> dict[str, str]:
    names = set(RENDER_THEMES_CHARS.keys())
    if name not in names:
        raise KeyError("" \
            f"Unknown theme '{name}'. \
            Available: {names}" \
            "")
    return RENDER_THEMES_CHARS[name]


def get_theme_colors(name: str) -> dict[str, str]:
    names = set(RENDER_THEMES_COLORS.keys())
    if name not in names:
        raise KeyError("" \
            f"Unknown theme '{name}'. \
            Available: {names}" \
            "")
    return RENDER_THEMES_COLORS[name]