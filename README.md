*This project has been created as part of the 42 curriculum by durisosa, and sasilves.*

<img width="1670" height="1466" alt="demo" src="https://github.com/user-attachments/assets/446443f6-2de8-4b08-8aaf-c79d4446f8bb" />
<img width="400" height="225" alt="demo" src="https://github.com/user-attachments/assets/3e64b165-b749-4451-bfb0-8dd3f1199db3" />

# 🧩 A-Maze-Ing

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/42-curriculum-black" alt="42 curriculum">
  <img src="https://img.shields.io/badge/Algorithms-maze%20generation-6f42c1" alt="Maze generation">
  <img src="https://img.shields.io/badge/Package-mazegen-blue" alt="mazegen package">
</p>

**A-Maze-Ing** is a Python maze generator, solver, visualizer, and small terminal game. It reads a configuration file, generates a maze, calculates a route from the entry to the exit, renders the result in the terminal, and exports the maze in the project's hexadecimal wall format.

The project combines graph theory, randomized algorithms, pathfinding, configuration validation, terminal rendering, and Python package design.

## Contents

- [Features](#features)
- [Program flow](#program-flow)
- [Maze and graph concepts](#maze-and-graph-concepts)
- [Maze generation algorithms](#maze-generation-algorithms)
- [Solving algorithms](#solving-algorithms)
- [Maze representation and the 42 pattern](#maze-representation-and-the-42-pattern)
- [Rendering and interactive mode](#rendering-and-interactive-mode)
- [Installation and usage](#installation-and-usage)
- [Configuration](#configuration)
- [Export format](#export-format)
- [Project structure](#project-structure)
- [Using the `mazegen` package](#using-the-mazegen-package)
- [Development commands and testing](#development-commands-and-testing)
- [Resources](#resources)
- [AI usage](#ai-usage)

## Features

- Perfect and imperfect maze generation.
- Reproducible generation using a configurable random seed.
- Three generation algorithms: Hunt-and-Kill, iterative DFS (Recursive Backtracker), and Randomized Prim.
- Three solving algorithms: Breadth-First Search (BFS), Depth-First Search (DFS), and A*.
- A centered `42` pattern made from blocked cells when the maze is large enough.
- ASCII/Unicode terminal rendering, with optional color and animation.
- Interactive menu to regenerate the maze, edit settings, and show or hide the solution.
- Play mode with keyboard movement.
- Export to a hexadecimal wall format, including entry, exit, and solution path.
- A reusable `mazegen` Python package, separated from the terminal application.
- Configuration validation and readable error messages.

## Program flow

The application separates configuration, maze logic, solving, output, and interaction.

```text
config.txt (or a supplied configuration path)
        |
        v
MazeConfiguration
        |
        v
MazeGenerator + selected generation strategy
        |
        v
Maze model and optional imperfect-maze processing
        |
        v
Selected solution strategy (BFS / DFS / A*)
        |
        v
Terminal renderer and interactive menu
        |
        v
Hexadecimal export (output.txt)
```

Configuration parsing is kept outside the reusable `mazegen` package. The package owns the maze model, generation and solving algorithms, `42` pattern, imperfect-maze logic, and export. The application layer handles configuration, terminal display, menus, keyboard input, and play mode.

## Maze and graph concepts

A maze can be modelled as a graph:

- **Vertex:** a traversable cell in the grid.
- **Edge:** an open passage between two adjacent cells.
- **Wall:** a blocked connection that prevents movement between cells.
- **Path:** a sequence of connected cells from the entry to the exit.
- **Cycle:** a route that loops back to an already reachable cell without retracing the same path.

A **perfect maze** has exactly one path between any two traversable cells in its connected region. Its passage graph is a tree: it is connected and contains no cycles. An **imperfect maze** has additional passages and therefore loops, creating alternative routes.

The maze is stored as a grid of `Cell` objects. Each cell tracks its coordinates, blocked state, and four walls: North, East, South, and West. Opening a passage is done through `Maze.remove_wall()`, which updates both adjacent cells. This avoids inconsistent one-sided walls.

## Maze generation algorithms

The project offers three generation strategies. They share the same maze interface and avoid cells blocked by the `42` pattern.

| Algorithm | How it works | Main characteristic |
|---|---|---|
| `HUNT_AND_KILL` | Walk randomly to unvisited neighbours. When trapped, scan for an unvisited cell next to the visited region and resume from there. | Iterative and does not require recursive calls. |
| `DFS` | The Recursive Backtracker strategy implemented iteratively with an explicit stack. Explore deeply, then backtrack when no unvisited neighbour remains. | Straightforward depth-first traversal; avoids Python recursion limits. |
| `PRIM` | Grow the maze from a starting cell by repeatedly selecting a cell from the frontier and connecting it to the existing maze. | Builds the maze outward through a randomized frontier. |

### Implementation strategy

Each generation strategy operates on the shared `Maze` model rather than manipulating the grid's internal matrix directly. The generator chooses the configured strategy, while the maze model provides the operations needed to inspect cells and open passages. This keeps algorithm-specific decisions separate from storage and rendering.

A typical generation process is:

1. Initialize the grid with its walls closed and mark any blocked pattern cells.
2. Choose a valid starting cell.
3. Apply the selected algorithm to open passages between valid adjacent cells.
4. Preserve the blocked cells and keep shared wall state consistent.
5. If imperfect mode is enabled, open additional safe passages according to the project's constraints.
6. Calculate a route from the entry to the exit using the selected solver.
7. Render the result and export it when requested.

### Perfect and imperfect modes

With `PERFECT=true`, generation leaves the base maze without adding extra connections afterwards. The resulting connected passage graph is tree-like and has a unique route between connected cells.

With `PERFECT=false`, the generator first creates the base maze and then opens additional safe walls. The imperfect-maze logic aims to:

- create at least two loops;
- reduce dead ends to at most two when possible under the project constraints;
- make the four corners and maze centre traversable as corridors;
- reject openings that would create a completely open `3 × 3` area;
- never open a passage through a blocked `42` cell.

Since this stage adds passages rather than closing existing ones, it does not disconnect the already connected maze.

## Solving algorithms

After generation, the selected solver searches for a route from the entry to the exit.

| Solver | Description | Path property |
|---|---|---|
| `bfs` | Breadth-First Search explores reachable cells level by level. | Finds a shortest path in an unweighted maze. |
| `dfs` | Depth-First Search explores one branch deeply before backtracking. | Finds a valid path, but not necessarily the shortest. |
| `astar` | A* uses Manhattan distance to guide the search toward the exit. | Finds a shortest path when used with the project's grid movement and admissible Manhattan heuristic. |

The solution is represented as a sequence of `N`, `E`, `S`, and `W` directions and as solution coordinates that the renderer can use to overlay the path on the maze.

## Maze representation and the 42 pattern

The maze uses four wall flags per cell: North, East, South, and West. A passage is opened by removing the corresponding wall from both adjacent cells, so neighbouring cells agree about whether they are connected.

The fixed `42` pattern is represented by blocked cells and is centered automatically when the maze is large enough. With its one-cell margin, it requires at least a `9 × 7` maze. Generation algorithms cannot enter blocked cells or open passages through them. If the configured entry or exit would land inside the pattern, it is redirected to a safe position before generation continues.

## Rendering and interactive mode

Rendering is kept separate from maze generation. `MazeGenerator` exposes events so the application can observe changes without coupling algorithm code to the terminal interface:

- `cell_updated` — emitted while generation or imperfect-maze processing changes the maze;
- `maze_completed` — emitted after generation finishes;
- `maze_solution` — emitted after the solution has been calculated.

When animation is enabled, the renderer responds to `cell_updated`; otherwise, it renders the completed maze once. The configuration includes ASCII and MLX render-mode values, although the current version handles both values through the terminal renderer.

### Interactive menu

| Key | Action |
|---|---|
| `O` | Show or hide the solution. |
| `E` | Edit the current maze configuration. |
| `G` | Generate a new maze. |
| `P` | Enter play mode. |
| `Q` | Export the maze and quit. |

The configuration menu can change dimensions, generation and solution algorithms, perfect mode, entry and exit, animation, color, delay, seed, output file, and display options.

### Play mode

The player starts at the configured entry and moves through open passages using `W`, `A`, `S`, `D` or the arrow keys. The solution can be toggled during play. Reaching the exit generates a new maze and increases the game score.

## Installation and usage

### Requirements

- Python 3.10 or newer
- Poetry
- `make`
- A terminal compatible with the keyboard controls used in interactive mode

### Install

Run from the repository root:

```bash
make install
```

This builds the local `mazegen` package and installs the project dependencies with Poetry.

### Run with the default configuration

```bash
poetry run make run
```

### Run with a custom configuration file

```bash
poetry run python3 a_maze_ing.py my_config.txt
```

If no configuration file is supplied, the application creates and uses an internal default configuration rather than crashing.

## Configuration

The configuration file uses one uppercase `KEY=VALUE` pair per line. Lines beginning with `#` are comments. Duplicate or invalid keys are rejected, and missing options are completed with their default values.

Example:

```ini
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
|---|---|---|
| `WIDTH` | Maze width in cells; valid range is 5–250. | `WIDTH=20` |
| `HEIGHT` | Maze height in cells; valid range is 5–250. | `HEIGHT=15` |
| `ENTRY` | Entry coordinate as `x,y`. | `ENTRY=0,0` |
| `EXIT` | Exit coordinate as `x,y`. | `EXIT=19,14` |
| `OUTPUT_FILE` | File used for maze export. | `OUTPUT_FILE=output.txt` |
| `PERFECT` | Enables or disables imperfect-maze processing. | `PERFECT=false` |

### Additional options

| Key | Values | Default |
|---|---|---|
| `ALGORITHM` | `HUNT_AND_KILL`, `DFS`, `PRIM` | `PRIM` |
| `SOLUTION_ALGORITHM` | `bfs`, `dfs`, `astar` | `astar` |
| `SEED` | Non-negative integer | `0` |
| `RENDER_MODE` | `ascii`, `mlx` | `ascii` |
| `ANIMATED` | Boolean | `true` |
| `COLOR` | Boolean | `false` |
| `DELAY` | Animation delay in seconds | `0.0025` |
| `PRETTY` | Boolean presentation messages | `false` |

Invalid entry or exit coordinates are redirected to valid positions. If entry and exit are equal, the exit is redirected to the bottom-right cell.

## Export format

The configured `OUTPUT_FILE` contains the maze rows, entry coordinate, exit coordinate, and solution path.

```text
<hexadecimal maze rows>

<entry x,y>
<exit x,y>
<solution using N/E/S/W>
```

Example format:

```text
9553
8552
c456

0,0
3,2
EESSW
```

The sample values above illustrate the format; actual rows, coordinates, and path depend on the generated maze and configuration. The exported solution is produced by the selected solver. If `DFS` is selected, the path is the one found by the DFS solver.

Each cell is encoded as one hexadecimal digit. Closed walls use these bit values:

| Wall | Value |
|---|---:|
| North | `1` |
| East | `2` |
| South | `4` |
| West | `8` |

The values of the closed walls are added together. For example, hexadecimal `f` represents a cell with all four walls closed.

## Project structure

```text
A-Maze-Ing/
├── src/
│   ├── config/          # configuration parsing and validation
│   ├── exception/      # application exceptions
│   ├── player/         # menus, keyboard handling and play mode
│   ├── render/         # terminal rendering
│   └── a_maze_ing.py   # application entry point
├── mazegen/
│   ├── mazegen/
│   │   ├── algorithm/  # generation strategies
│   │   ├── model/      # Cell, Maze and MazeGenerator
│   │   ├── pattern/    # centered 42 pattern
│   │   └── solver/     # BFS, DFS and A*
│   └── pyproject.toml
├── config.txt
├── Makefile
├── pyproject.toml
└── README.md
```

## Using the `mazegen` package

The maze-generation logic is packaged separately from the terminal application and can be installed independently:

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

## Development commands and testing

The repository's Makefile provides these commands:

```bash
make debug
make lint
make lint-strict
make clean
```

- `debug` — runs the program and redirects errors to `log.txt`.
- `lint` — runs `flake8` and `mypy`.
- `lint-strict` — also runs `mypy --strict`.
- `clean` — removes caches and generated build files.

Run the test suite if tests are configured in the checkout:

```bash
poetry run pytest
```

Configuration validation should cover missing or unreadable files, malformed `KEY=VALUE` lines, duplicate or unknown keys, invalid dimensions and coordinates, invalid enum or boolean values, and invalid output file names. The application also handles renderer errors and keyboard interruptions such as `Ctrl+C` and `Ctrl+D`.

## Resources

These resources are useful for understanding the algorithms and implementation:

- [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/) — packaging Python code.
- [Python `random` documentation](https://docs.python.org/3/library/random.html) — reproducible pseudo-random generation and seeds.
- [Using Python to Create and Solve Mazes](https://medium.com/@msgold/using-python-to-create-and-solve-mazes-672285723c96) — a practical maze example.
- [ASCII maze rendering discussion](https://codereview.stackexchange.com/questions/263517/more-efficient-way-to-create-an-ascii-maze-using-box-characters) — terminal rendering approaches.
- [Maze printing discussion](https://stackoverflow.com/questions/55452329/print-a-maze-using-only-two-characters) — a simple representation example.
- [Discrete Mathematics: An Open Introduction](https://discrete.openmathbooks.org/) — background on graphs and discrete structures.
- [pytest documentation](https://docs.pytest.org/) — Python testing.

## AI usage

Artificial intelligence tools were used as development support, mainly for research, debugging, comparing algorithm approaches, explaining graph and pathfinding concepts, and improving documentation.

AI-generated suggestions were treated as assistance rather than a substitute for understanding or testing the project. The implementation, configuration options, algorithm descriptions, and final README should be checked against the actual source code by the project authors.
