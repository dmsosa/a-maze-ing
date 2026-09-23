# Usage: poll in a game loop
import time
from render.utils import getch


def main() -> None:
    while True:
        key = getch()
        if key:
            print(f"Key: {repr(key)}")
        time.sleep(0.05)


if __name__ == "__main__":
    main()
