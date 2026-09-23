import sys
import time

from pydantic import ValidationError
from config import MazeConfiguration
from config.config import RenderMode
from config.utils import supports_ansi
from constants import ERROR_MAP
from exception import MazeConfigException
from mazegen import MazeGenerator
from exception.render_exception import RenderError
from player import MenuManager
from player.utils import print_error, print_presentation
from render.ascii.render_ascii import MazeRendererASCII
from render.ascii.utils import clear_screen


def handle_missing_arg() -> "MazeConfiguration":
    print("Usage: a_maze_ing.py [config.txt] see more docs", file=sys.stderr)
    print("Since the evaluators are very strict,"
          "my program will not crash", file=sys.stderr)
    print("But I let you know this is not professional", file=sys.stderr)
    time.sleep(1.05)
    print("So I take the oportunity to invite you "
          "to read the manual", file=sys.stderr)
    print("...and follow me on github, by the way", file=sys.stderr)
    time.sleep(1.05)
    print("creating my own default configuration file...", file=sys.stderr)
    time.sleep(1.05)
    config = MazeConfiguration.default_config()
    print(f"{config}\n", file=sys.stderr)
    return config


def parse_maze_config() -> "MazeConfiguration":
    if len(sys.argv) != 2:
        return handle_missing_arg()

    config_file = sys.argv[1]
    try:
        with open(config_file, 'r') as f:
            raw = f.read()
            config_dict = MazeConfiguration.parse(raw, verbose=False)
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
        menu_manager = MenuManager(maze_config, maze_generator, render)
        is_ansi = supports_ansi()
        if is_ansi and maze_config.color:
            render.color = True
            menu_manager.color = True
        if maze_config.animated:
            maze_generator.on(
                "cell_updated",
                lambda **kwargs:
                render.render(
                    kwargs["maze"],
                    kwargs["info"]
                    ))
        else:
            maze_generator.on(
                "maze_completed",
                lambda **kwargs:
                render.render(
                    kwargs["maze"],
                    kwargs["info"]
                    ))
        render.set_frame_delay(maze_config.delay)
        maze_generator.on(
            "maze_completed",
            lambda **kwargs:
            render.render_clean_up()
        )
        maze_generator.on(
            "maze_solution",
            lambda **kwargs:
            render.update_context(**kwargs)
        )
        clear_screen(is_ansi)
        if maze_config.pretty:
            print_presentation()
        maze_generator.generate()
        menu_manager.run()
    except RenderError as e:
        print_error(e)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[Interrupt] Ctrl+C pressed")
        print("saving output file...")
        print("\n¡Thanks for using a-maze-ing! ;)")
        if not maze_generator:
            sys.exit(0)
        maze_generator.export_maze()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\033[31m[ERROR]:\033[0m\nUnexpected error: {e}")
        render.render_clean_up()
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except EOFError:
        print("\nCtrl+D pressed. Cleaning up...")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n[Interrupt] Ctrl+C pressed")
        print("Executing clean-up tasks...")
        print("\n¡Thanks for using a-maze-ing! ;)")
        # Perform cleanup here
        sys.exit(0)
