*This project has been created as part of the 42 curriculum by durisosa, sasilves.*

# A-Maze-Ing

## Description

A-Maze-Ing is a Python maze generator, solver, visualizer, and small terminal game.
The program reads a configuration file, generates a maze, solves it, displays it in the terminal, and exports it using the hexadecimal wall format required by the project.

The project is divided into two main parts:

- `mazegen/`: reusable package containing the maze model, generation algorithms, solving algorithms, `42` pattern, imperfect-maze logic, and export logic.
- `src/`: application layer containing configuration parsing, terminal rendering, menus, input handling, and play mode.

Main features:

- Perfect and imperfect maze generation.
- Reproducible generation using a seed.
- Centered `42` pattern built with blocked cells when the maze is large enough.
- Three generation algorithms: Hunt-and-Kill, Recursive Backtracker, and Randomized Prim.
- Three solving algorithms: BFS, DFS, and A*.
- ASCII/Unicode terminal rendering with optional colors and animation.
- Interactive menu to regenerate the maze, edit configuration, and show/hide the solution.
- Playable mode using keyboard movement.
- Hexadecimal export containing the maze, entry, exit, and solution path.
- Reusable `mazegen` Python package.

## Program flow

The application follows this general flow:

```text
config.txt
    ↓
MazeConfiguration
    ↓
MazeGenerator
    ↓
Maze + Generation Strategy
    ↓
Perfect / Imperfect processing
    ↓
Solution Strategy
    ↓
Renderer / Interactive Menu
    ↓
output.txt
```

Configuration parsing is kept outside the reusable `mazegen` package. The package is responsible for the maze structure, algorithms, solving, pattern, and export, while the application layer handles user interaction and visualization.

## Instructions

### Requirements

- Python 3.10 or newer.
- Poetry.
- `make`.
- A terminal compatible with the keyboard controls used by the interactive mode.

### Installation

From the repository root:

```bash
make install
```

This builds the local `mazegen` package and installs the project dependencies with Poetry.

### Run

Using the default `config.txt`:

```bash
poetry run make run
```

Using another configuration file:

```bash
poetry run python3 a_maze_ing.py my_config.txt
```

If no configuration file is supplied, the application creates and uses an internal default configuration instead of crashing.

### Other Makefile commands

```bash
make debug
make lint
make lint-strict
make clean
```

- `debug`: runs the program and redirects errors to `log.txt`.
- `lint`: runs `flake8` and `mypy`.
- `lint-strict`: also runs `mypy --strict`.
- `clean`: removes caches and generated build files.

## Configuration file

The configuration file uses one uppercase `KEY=VALUE` pair per line.
Lines beginning with `#` are comments. Duplicate or invalid keys are rejected, while missing options are completed with their default values.

Example:

```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
ALGORITHM=PRIM
SOLUTION_ALGORITHM=astar
SEED=42
OUTPUT_FILE=output.txt
PERFECT=true
RENDER_MODE=ascii
DELAY=0.0025
COLOR=true
ANIMATED=false
```

### Core options

| Key | Description | Example |
| --- | --- | --- |
| `WIDTH` | Maze width in cells. Valid application range: 5-250. | `WIDTH=20` |
| `HEIGHT` | Maze height in cells. Valid application range: 5-250. | `HEIGHT=15` |
| `ENTRY` | Entry coordinate as `x,y`. | `ENTRY=0,0` |
| `EXIT` | Exit coordinate as `x,y`. | `EXIT=19,14` |
| `OUTPUT_FILE` | File used for maze export. | `OUTPUT_FILE=output.txt` |
| `PERFECT` | Enables or disables imperfect-maze processing. | `PERFECT=false` |

### Additional options

| Key | Values | Default |
| --- | --- | --- |
| `ALGORITHM` | `HUNT_AND_KILL`, `DFS`, `PRIM` | `PRIM` |
| `SOLUTION_ALGORITHM` | `bfs`, `dfs`, `astar` | `astar` |
| `SEED` | Non-negative integer | `0` |
| `RENDER_MODE` | `ascii`, `mlx` | `ascii` |
| `ANIMATED` | Boolean | `true` |
| `COLOR` | Boolean | `false` |
| `DELAY` | Animation delay in seconds | `0.0025` |
| `PRETTY` | Boolean presentation messages | `false` |

Invalid entry or exit coordinates are redirected to valid positions. If entry and exit are equal, the exit is redirected to the bottom-right cell. In the current version, both `ascii` and `mlx` configuration values are handled by the terminal renderer.

## Maze representation

The maze is represented as a grid of `Cell` objects. Each cell stores its coordinates, blocked state, and four walls: North, East, South, and West.

Opening a passage is always performed through `Maze.remove_wall()`, which updates both adjacent cells. This keeps the maze representation coherent and prevents one-sided walls.

Generation and solving algorithms interact with the maze through its public methods rather than modifying the internal matrix directly.

## Maze generation

Three generation strategies are available.

| Algorithm | Description |
| --- | --- |
| `HUNT_AND_KILL` | Performs a random walk through unvisited cells and then searches for a new unvisited cell connected to the visited region. |
| `DFS` | Recursive Backtracker implemented iteratively with a stack. It explores deeply and backtracks when no unvisited neighbor remains. |
| `PRIM` | Randomized Prim algorithm. It grows the maze by repeatedly selecting cells from a frontier. |

All strategies operate on the same `Maze` interface and ignore cells blocked by the `42` pattern.

### Perfect maze

With `PERFECT=true`, the selected generation algorithm creates the maze without adding extra connections afterwards. The accessible maze remains tree-like, providing one unique route between connected cells.

### Imperfect maze

With `PERFECT=false`, the generator first creates the base maze and then opens additional safe walls.

The imperfect-maze logic is designed to:

- create at least two loops;
- reduce dead ends to at most two when possible under the project constraints;
- make the four corners and the maze center traversable as corridors;
- reject openings that would create a completely open `3x3` area;
- never open a passage through a blocked `42` cell.

Because imperfect mode only removes walls from an already connected maze, adding these extra connections does not disconnect the existing maze.

## The `42` pattern

The project contains a fixed `42` pattern represented by blocked cells.

The pattern is centered automatically when the maze is large enough. With its one-cell margin, it requires a maze of at least `9x7` cells.

Blocked cells cannot be entered by generation algorithms and their walls cannot be opened. If entry or exit would fall inside the pattern, they are redirected to safe corner positions before generation continues.

## Solving algorithms

After generation, the configured solver finds a route from entry to exit.

| Solver | Description |
| --- | --- |
| `bfs` | Breadth-First Search. Explores level by level and finds a shortest path in the unweighted maze. |
| `dfs` | Depth-First Search. Explores one branch deeply and returns a valid path, which is not necessarily the shortest. |
| `astar` | A* using Manhattan distance as its heuristic. It finds a shortest path while guiding exploration toward the exit. |

The solution is stored as a string made of `N`, `E`, `S`, and `W` directions and as a set of solution coordinates used by the renderer.

## Rendering and events

Rendering is intentionally separated from maze generation.

`MazeGenerator` exposes a small event system that allows the application to observe the generation process without coupling the algorithms to the renderer.

The main events are:

- `cell_updated`: emitted while generation or imperfect-maze processing changes the maze;
- `maze_completed`: emitted after generation is complete;
- `maze_solution`: emitted when the solution path has been calculated.

When animation is enabled, the renderer reacts to `cell_updated`. Otherwise, it renders the completed maze only once.

This separation allows the internal generation algorithms to remain reusable independently of the terminal interface.

## Interactive menu

After generation, the application enters an interactive menu.

| Key | Action |
| --- | --- |
| `O` | Show or hide the solution. |
| `E` | Edit the current maze configuration. |
| `G` | Generate a new maze. |
| `P` | Enter play mode. |
| `Q` | Export the maze and quit. |

The configuration menu can modify dimensions, generation and solution algorithms, perfect mode, entry and exit, animation, color, delay, seed, output file, and display theme options.

### Play mode

The generated maze can also be played directly from the terminal.

The player starts from the configured entry and moves through open passages using `W`, `A`, `S`, `D` or the arrow keys. The solution can be toggled while playing, and reaching the exit generates a new maze and increases the game score.

## Error handling

The application validates both configuration syntax and configuration values before generating the maze.

It handles errors such as:

- missing or unreadable configuration files;
- invalid `KEY=VALUE` syntax;
- duplicated or unknown configuration keys;
- invalid dimensions or coordinates;
- invalid enum or boolean values;
- invalid output file names;
- renderer errors;
- `Ctrl+C` and `Ctrl+D` during interactive use.

Known configuration problems are reported with a clear error message instead of allowing the program to fail silently.

## Output format

When the maze is exported, `OUTPUT_FILE` contains:

```text
<hexadecimal maze rows>

<entry x,y>
<exit x,y>
<solution using N/E/S/W>
```

Example:

```text
9553
8552
c456

0,0
3,2
EESSW
```

> **Solution export:** the solution written to `OUTPUT_FILE` is generated with the currently selected solution algorithm. When `DFS` is selected, the exported `N/E/S/W` path is the path found by the DFS solver.

Each cell is represented by one hexadecimal digit. Closed walls use the following bit values:

| Wall | Value |
| --- | ---: |
| North | `1` |
| East | `2` |
| South | `4` |
| West | `8` |

The values of the closed walls are added together. For example, hexadecimal `f` represents a cell with all four walls closed.

## Reusable `mazegen` package

The maze-generation logic is packaged separately from the terminal application and can be installed independently.

```bash
python3 -m pip install ./mazegen
```

Example:

```python
from mazegen import MazeGenerator, MazeAlgorithm, SolutionAlgorithm

generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    algorithm=MazeAlgorithm.PRIM,
    solution_algorithm=SolutionAlgorithm.ASTAR,
    seed=42,
    perfect=True,
    output_file="output.txt",
)

maze = generator.generate()

generator.export_maze()
print("\n".join(maze.hex_digits))
print(generator.solution_path)
```

More details about the package architecture and public API are available in [`mazegen/README.md`](mazegen/README.md).

## Project structure

```text
A-Maze-Ing/
├── src/
│   ├── config/          # configuration parsing and validation
│   ├── exception/       # application exceptions
│   ├── player/          # menus, keyboard handling and play mode
│   ├── render/          # terminal rendering
│   └── a_maze_ing.py    # application entry point
├── mazegen/
│   ├── mazegen/
│   │   ├── algorithm/   # generation strategies
│   │   ├── model/       # Cell, Maze and MazeGenerator
│   │   ├── pattern/     # centered 42 pattern
│   │   └── solver/      # BFS, DFS and A*
│   └── pyproject.toml
├── config.txt
├── Makefile
├── pyproject.toml
└── README.md
```

## Resources

The following references were used during development:

- Python Packaging User Guide: https://packaging.python.org/en/latest/tutorials/packaging-projects/
- Python maze generation and solving example: https://medium.com/@msgold/using-python-to-create-and-solve-mazes-672285723c96
- ASCII maze rendering discussion: https://codereview.stackexchange.com/questions/263517/more-efficient-way-to-create-an-ascii-maze-using-box-characters
- Maze printing discussion: https://stackoverflow.com/questions/55452329/print-a-maze-using-only-two-characters

## AI usage

Artificial intelligence tools were used as support during the development process, mainly for research, debugging, and documentation.
