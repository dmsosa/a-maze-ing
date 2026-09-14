import platform, \
sys, \
termios, \
tty, \
time


def get_key():
    if sys.platform == "win32":
        import msvcrt
        key = msvcrt.getch()
        return key.decode("utf-8")
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key


HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


def print_line(s, delay=0.05) -> None:
    for ch in s:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)


def erase_line(s) -> None:
    sys.stdout.write("\r" + " " * len(s) + "\r")
    sys.stdout.flush()


def print_presentation() -> None:
    print_line(f"{YELLOW}{MAIN_INSTRUCTION}{RESET}")
    erase_line(MAIN_INSTRUCTION)
    print_line(f"{BOLD}{GREEN}{TITLE}{RESET}")
    print_line(f"{BOLD}{GREEN}{SUBTITLE}{RESET}")
