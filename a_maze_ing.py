import sys

from mazegen import MazeConfigException, MazeConfiguration


def parse_maze_config() -> dict[str, str]:
    argvlen: int = len(sys.argv)
    if (argvlen != 2):
        print("Usage: a_maze_ing.py [config.txt] see more docs")
        sys.exit(1)
    config_file = sys.argv[1]
    try:
        with open(config_file, 'r') as f:
            raw = f.read()
            maze_config = MazeConfiguration.parse(raw)
            return maze_config
    except FileNotFoundError as e:
        msg = "\033[31m[ERROR]:\033[0m\n"
        msg += f"The file '{config_file}' does not exist."
        print(f"{e}\n{msg}")
    except PermissionError as e:
        msg = "\033[31m[ERROR]:\033[0m\n"
        msg += f"Permission denied to read '{config_file}'."
        print(f"{e}\n{msg}")
    except MazeConfigException as e:
        print(f"\033[31mMazeConfigException\033[\n0m{e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return dict()


def main() -> None:
    maze_config = parse_maze_config()
    print(maze_config)


if __name__ == "__main__":
    main()
