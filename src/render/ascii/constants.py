CELL_WIDTH = 3

RENDER_THEMES_CHARS: dict[str, dict[str, str]] = {
    "classic": {
        "wall_n":  "─"*CELL_WIDTH,
        "wall_w": "│",
        "space":       " "*CELL_WIDTH,
        "corner":    "*",
        "current": "@".center(CELL_WIDTH, " "),
        "visited": "·".center(CELL_WIDTH, " "),
        "solution": "~".center(CELL_WIDTH, " "),
        "hunt_pos": "?".center(CELL_WIDTH, " "),
        "blocked":   "█"*CELL_WIDTH,
        "player":     "🚶🏻‍➡️".center(CELL_WIDTH, " "),
        "entry":      "🚪".center(CELL_WIDTH, " "),
        "exit_":       "🔑".center(CELL_WIDTH, " "),
    },
    "block": {
        "wall_n":  "▓"*CELL_WIDTH,
        "wall_w": "▓",
        "way":       "░",
        "space":       " "*CELL_WIDTH,
        "corner":    "▓",
        "blocked":   "█",
        "player":     "🚶🏻‍➡️",
        "entry":      "🚪",
        "exit_":       "🔑",
    },
}

CORNER_CHARS = {
    0b0000: " ",
    0b0001: "╵", 0b0010: "╶", 0b0011: "└",
    0b0100: "╷", 0b0101: "│", 0b0110: "┌", 0b0111: "├",
    0b1000: "╴", 0b1001: "┘", 0b1010: "─", 0b1011: "┴",
    0b1100: "┐", 0b1101: "┤", 0b1110: "┬", 0b1111: "┼",
}

RENDER_THEMES_COLORS: dict[str, dict[str, str]] = {
    "classic": {
        "bg": "#757575",
        "wall": "#e94560",
        "way": "#58e945",
        "current":  "#0f3460",
        "visited":   "#A06FE8",
        "solution":   "#533483",
        "hunt_pos": "#81aadc",
        "special":    "#e94560",
    },
    "matrix": {
        "bg": "#000000",
        "wall":       "#003300",
        "current":  "#00ff41",
        "entry":      "#00cc33",
        "exit_":       "#ffffff",
        "way":        "#008822",
        "special":    "#005500",
    },
    "ocean": {
        "bg": "#0a1628",
        "wall":       "#1e90ff",
        "current":  "#ffd700",
        "entry":      "#40e0d0",
        "exit_":       "#ff6347",
        "way":        "#4682b4",
        "special":    "#00bfff",
    },
    "sunset": {
        "bg": "#2d1b4e",
        "wall":       "#ff6b35",
        "current":  "#ffd93d",
        "entry":      "#6bcb77",
        "exit_":       "#ff477e",
        "way":        "#c77dff",
        "special":    "#ff9e00",
    },
    "minimal": {
        "bg": "#f8f9fa",
        "wall":       "#212529",
        "current":  "#0d6efd",
        "entry":      "#198754",
        "exit_":       "#dc3545",
        "way":        "#6c757d",
        "special":    "#adb5bd",
    },
    "neon": {
        "bg": "#0d0d0d",
        "wall":       "#ff00ff",
        "current":  "#00ffff",
        "entry":      "#39ff14",
        "exit_":       "#ff073a",
        "way":        "#ffe600",
        "special":    "#ff00ff",
    },
    "forest": {
        "bg": "#1b2a1b",
        "wall":       "#4a7c59",
        "current":  "#f4e285",
        "entry":      "#a8e6cf",
        "exit_":       "#d4a373",
        "way":        "#52796f",
        "special":    "#355e3b",
    },
    "ice": {
        "bg": "#0b132b",
        "wall":       "#3a506b",
        "current":  "#dff9fb",
        "entry":      "#a3cef1",
        "exit_":       "#ff595e",
        "way":        "#5bc0be",
        "special":    "#1b262c",
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