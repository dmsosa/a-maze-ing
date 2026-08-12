import sys

def main() -> None:
    argvlen: int = len(sys.argv)
    if (argvlen < 2):
        print("Usage: a_maze_ing.py [config.txt] see more docs")
        sys.exit(1)
    after_flags: int = 1
    config_file = argv[after_flags]
    try:
        with open(config_file, 'r') as f:
            raw = f.read()
            # Here I try to create the maze itself. If it was successfully created, I can proceed to detect the strategy used
            # The entire logic needs to be done inside this try block? No, I can initialize the MazeGenerator as an abstract class with no info yet,
            # then initialize it with my config file, but it means parsing stuff with validation logic, yeah, it could be good
            # 
    except FileNotFoundError:
        print(f"Error: The file '{config_file}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied to read '{config_file}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()