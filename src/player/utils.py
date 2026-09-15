import sys, \
time

from player.constants import BOLD, CYAN, GREEN, RED, RESET, YELLOW


def print_line(s, delay=0.05) -> None:
    for ch in s:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)


def erase_line(s, delay=0.05) -> None:
    sys.stdout.write("\r")
    for ch in s:
        sys.stdout.write(" ")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\r")

# ── Message store ──────────────────────────────────────────────
MESSAGES = [
    # index 0 – title
    "Welcome to A MAZE ING! Good luck!",
    # index 1 – subtitle
    "Enjoy, and find your way ;)",
    # index 2 -- instructions
    "Use W/S or ↑/↓ to navigate. \
Type 'quit' to exit, Ctrl+C to interrupt, \
Ctrl+D for EOF.",
    # index 3 – goodbye
    "Thanks for playing A MAZE ING! You'll be back for more.",
    # index 4+ – motivation (success / failure)
    f"{BOLD}{GREEN}Nice move! Keep it up!{RESET}",
    f"{YELLOW}So close! Try a different path.{RESET}",
    f"{BOLD}{GREEN}You found it! Incredible reflexes!{RESET}",
    f"{BOLD}{RED}Dead end. Breathe and rethink.{RESET}",
    f"{BOLD}{CYAN}Almost there! Stay focused.{RESET}",
    f"{BOLD}{RED}Ouch! That wall bit back.{RESET}",
]

TITLE  = 0
SUBTITLE  = 1
INSTRUCTIONS  = 2
GOODBYE  = 3
MOTIVATE = list(range(4, len(MESSAGES)))   # indices for random pick


# ── Helper: ANSI "typing" illusion ─────────────────────────────
def _type_out(text: str, delay: float = 0.03) -> None:
    """Print *text* one character at a time (ANSI cursor tricks)."""
    print("\033[?25l", end="")          # hide cursor
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print("\033[?25h")                   # show cursor again
    print()                              # newline


def _plain(text: str) -> None:
    print(text)


# ── Public API ─────────────────────────────────────────────────
def print_presentation() -> None:
    print_line(f"{YELLOW}{MESSAGES[INSTRUCTIONS]}{RESET}")
    erase_line(MESSAGES[INSTRUCTIONS])
    print_line(f"{BOLD}{GREEN}{MESSAGES[TITLE]}{RESET}")
    erase_line(MESSAGES[TITLE])
    print_line(f"{BOLD}{GREEN}{MESSAGES[SUBTITLE]}{RESET}")

def print_goodbye(prettify: bool = True) -> None:
    _type_out(MESSAGES[GOODBYE]) if prettify else _plain(MESSAGES[GOODBYE])


def print_motivation(success: bool = True, prettify: bool = True) -> None:
    import random
    pool = MOTIVATE[::2] if success else MOTIVATE[1::2]
    msg = random.choice(pool)
    _type_out(msg) if prettify else _plain(msg)
