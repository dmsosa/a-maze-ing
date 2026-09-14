import sys

from pydantic import ValidationError
from config import MazeConfiguration
from config.config import RenderMode
from constants import ERROR_MAP
from exception import MazeConfigException
from mazegen import MazeGenerator
from exception.render_exception import supports_ansi
from render.ascii.render_ascii import MazeRendererASCII
from player.utils import print_presentation
from render.ascii.utils import show_cursor


def parse_maze_config() -> "MazeConfiguration":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: a_maze_ing.py [config.txt] see more docs")

    config_file = sys.argv[1]
    try:
        with open(config_file, 'r') as f:
            raw = f.read()
            config_dict = MazeConfiguration.parse(raw)
            return MazeConfiguration(**config_dict)
    except (
        FileNotFoundError,
        PermissionError,
        MazeConfigException,
        ValidationError
        ) as e:
        msg = ERROR_MAP[type(e)].format(file=sys.argv[1], e=e)
        print(f"\033[31m[ERROR]:\033[0m\n{msg}")
        sys.exit(1)


def main() -> None:
    try:
        maze_config = parse_maze_config()
        maze_generator = MazeGenerator(**maze_config.model_dump())
        if maze_config.render_mode == RenderMode.ASCII:
            render = MazeRendererASCII()
        elif maze_config.render_mode == RenderMode.MINILIBX:
            render = MazeRendererASCII()
        if supports_ansi() and maze_config.color:
            render.color = True
        if maze_config.animated:
            maze_generator.on(
                "cell_updated",
                lambda **kwargs: 
                render.render(
                    kwargs["generator"],
                    kwargs["maze"],
                    kwargs["info"]
                    ))
        else:
            maze_generator.on(
                "maze_completed",
                lambda **kwargs: 
                render.render(
                    kwargs["generator"],
                    kwargs["maze"],
                    kwargs["info"]
                    ))
        render.set_frame_delay(maze_config.delay)
        if maze_config.pretty:
            print_presentation()
        maze = maze_generator.generate()
        while True:
            key = render.render_menu()
            if key == "1":
                render.play(maze)
            elif key == "2":
                maze_generator.seed = (maze_generator.seed or 0) + 1
                maze = maze_generator.generate()
            elif key == "3":
                print("Thanks for playing a_maze_ing! See you next time.")
                break
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\033[31m[ERROR]:\033[0m\nUnexpected error: {e}")
        render.render_clean_up()
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Safety net: catches Ctrl+C that fires *outside* the input() call
        # (e.g. during processing between prompts)
        print("\n[Interrupted]")
        sys.exit(130)  # conventional exit code for SIGINT

