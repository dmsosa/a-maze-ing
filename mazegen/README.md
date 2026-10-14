*This project has been created as part of the 42 curriculum by durisosa, sasilves.*

# mazegen

`mazegen` is the reusable maze-generation package used by A-Maze-Ing.
It contains the maze model, generation algorithms, solving algorithms, centered `42` pattern, imperfect-maze processing, event system, and hexadecimal export logic without depending on the terminal user interface.

## Architecture overview

```text
MazeGenerator
      │
      ├── creates ─────→ Maze
      │                    │
      │                    └── contains → Cell
      │
      ├── uses ───────→ Generation Strategy
      ├── uses ───────→ Solution Strategy
      ├── applies ─────→ 42 Pattern
      ├── emits ───────→ Events
      └── exports ─────→ Hexadecimal Output
```

The package separates maze structure from the algorithms that operate on it.

| Component | Responsibility |
| --- | --- |
| `Cell` | Represents one maze cell, its coordinates, walls, and blocked state. |
| `Maze` | Stores the complete grid and provides safe operations for accessing and modifying it. |
| `MazeGenerator` | Coordinates generation, imperfect processing, solving, events, and export. |
| `algorithm` | Contains maze-generation strategies. |
| `solver` | Contains maze-solving strategies. |
| `pattern` | Defines and centers the blocked `42` pattern. |
| `constants` | Defines available generation and solution algorithms. |

## Installation

From the A-Maze-Ing repository root:

```bash
python3 -m pip install ./mazegen
```

The package can also be built with Poetry:

```bash
cd mazegen
poetry build
```

It requires Python 3.10+ and Pydantic 2.

## Quick usage

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

print("\n".join(maze.hex_digits))
print(generator.solution_path)

generator.export_maze()
```

`generate()` initializes the maze, centers and blocks the `42` pattern when it fits, runs the selected generation strategy, optionally makes the maze imperfect, solves it, emits the corresponding events, and returns the resulting `Maze` object.

## Core components

### `Cell`

A `Cell` represents one position in the maze.

It stores:

- `x` and `y` coordinates;
- four wall states;
- whether the cell is blocked by the pattern.

Useful methods:

```python
cell.has_wall(direction)
cell.ctoh()
```

`ctoh()` converts the cell wall state to the hexadecimal representation used by the output format.

### `Maze`

`Maze` stores the two-dimensional grid and exposes the operations needed by generation and solving strategies.

```python
maze.get_cell(x, y)
maze.get_neighbors(x, y)
maze.get_available_neighbors(x, y)
maze.get_open_neighbors(x, y)
maze.remove_wall(x, y, direction)
maze.block_cells(positions)
maze.hex_digits
```

`get_neighbors()` returns all geometric neighbors inside the maze.

`get_available_neighbors()` removes blocked cells from that result and is mainly used during generation.

`get_open_neighbors()` only returns neighbors connected by an already open passage and is mainly used by solvers.

`remove_wall()` updates both sides of a connection. Generation strategies therefore do not need to manage wall symmetry themselves.

### `MazeGenerator`

`MazeGenerator` coordinates the complete maze lifecycle.

```text
Initialize Maze
      ↓
Center and block 42 pattern
      ↓
Run generation strategy
      ↓
Add loops if perfect=False
      ↓
Run solution strategy
      ↓
Emit completion / solution events
      ↓
Return Maze
```

Important fields:

| Field | Description |
| --- | --- |
| `width`, `height` | Maze dimensions. |
| `entry`, `exit` | Start and destination coordinates. |
| `algorithm` | Selected generation strategy. |
| `solution_algorithm` | Solver used after generation. |
| `seed` | Random seed used for reproducibility. |
| `perfect` | Enables or disables imperfect-maze processing. |
| `output_file` | Destination used by `export_maze()`. |
| `maze` | Generated `Maze` instance. |
| `solution_path` | Solution represented with `N/E/S/W`. |
| `solution_coords` | Coordinates belonging to the solution. |
| `blocked_positions` | Coordinates occupied by the centered pattern. |

Important methods:

| Method | Description |
| --- | --- |
| `generate()` | Generates and solves a maze. |
| `make_imperfect(maze)` | Opens safe extra passages to create loops. |
| `output_text()` | Builds the complete subject output as a string. |
| `export_maze()` | Writes the output to `output_file`. |
| `on(event, callback)` | Registers an event listener. |
| `off(event, callback)` | Removes an event listener. |

## Generation strategies

Generation algorithms inherit from `MazeAlgorithmStrategy` and work through the public `Maze` interface.

| Enum value | Algorithm | Main idea |
| --- | --- | --- |
| `MazeAlgorithm.HUNT_AND_KILL` | Hunt-and-Kill | Random walk through unvisited cells followed by a hunt for another unvisited cell connected to the visited region. |
| `MazeAlgorithm.DFS` | Recursive Backtracker | Depth-first exploration using an explicit stack and backtracking. |
| `MazeAlgorithm.PRIM` | Randomized Prim | Expands the visited region through randomly selected frontier cells. |

The strategy decides which cells should be connected. `Maze.remove_wall()` performs the structural modification and keeps both cell walls synchronized.

## Solving strategies

Solvers inherit from `MazeSolutionStrategy` and navigate the generated maze mainly through `Maze.get_open_neighbors()`.

| Enum value | Algorithm | Result |
| --- | --- | --- |
| `SolutionAlgorithm.BFS` | Breadth-First Search | Finds a shortest path in the unweighted maze. |
| `SolutionAlgorithm.DFS` | Depth-First Search | Finds a valid path, not necessarily the shortest. |
| `SolutionAlgorithm.ASTAR` | A* with Manhattan distance | Finds a shortest path while guiding exploration toward the exit. |

Each solver returns:

```python
(solution_path, solution_coords)
```

`solution_path` is a direction string such as `"EESSWN"` and `solution_coords` contains the coordinates visited by that solution.

## Perfect and imperfect mazes

With:

```python
perfect=True
```

no extra passages are added after the selected generation algorithm.

With:

```python
perfect=False
```

`make_imperfect()` opens additional walls while preserving the project constraints.

The method:

1. identifies the four corners and maze center as required corridor cells;
2. collects the remaining dead ends;
3. tries to open one safe additional connection from those cells;
4. rejects a connection if it would create a completely open `3x3` area;
5. adds more safe walls if fewer than two loops were created;
6. checks that required cells have at least two open connections;
7. verifies that no more than two dead ends remain.

Blocked `42` cells are automatically excluded because `Maze.get_available_neighbors()` does not return them and `Maze.remove_wall()` refuses to open a blocked cell.

Since the operation starts from an already connected maze and only removes walls, adding loops cannot disconnect the maze.

## `42` pattern

The pattern is defined in `pattern/forty_two.py` as coordinates relative to the maze center.

`centered_positions()` translates those relative coordinates to absolute maze coordinates while checking that the entire pattern and its margin fit inside the maze.

With the current pattern and one-cell margin, at least `9x7` cells are required.

The calculated positions are marked as blocked before the generation algorithm runs. Generation strategies therefore treat the `42` as an obstacle instead of generating passages through it.

## Event system

`MazeGenerator` inherits from a small `EventEmitter` implementation.

```python
generator.on(event, callback)
generator.off(event, callback)
```

The current generator emits:

- `cell_updated` while generation or imperfect processing changes the maze;
- `maze_completed` when maze generation is finished;
- `maze_solution` after the solver has produced its path.

Example:

```python
def on_solution(**data):
    print(data["solution_path"])


generator.on("maze_solution", on_solution)
generator.generate()
```

This event-based design keeps renderers outside the package algorithms. A renderer can observe state changes without `Cell`, `Maze`, or the strategies depending on display code.

## Hexadecimal wall encoding

Every cell is encoded using four wall bits:

| Direction | Value |
| --- | ---: |
| North | `1` |
| East | `2` |
| South | `4` |
| West | `8` |

Examples:

- `0`: no closed walls;
- `1`: North wall only;
- `3`: North + East;
- `f`: all four walls closed.

`maze.hex_digits` returns the complete maze as one hexadecimal string per row.

## Export format

`generator.output_text()` returns:

```text
<hexadecimal maze rows>

<entry x,y>
<exit x,y>
<solution path>
```

`generator.export_maze()` writes exactly that content to `output_file` using UTF-8 and Unix newlines.

> **Solution export:** the exported solution always corresponds to the currently selected solver. If `SolutionAlgorithm.DFS` is selected, the final `N/E/S/W` line is the path found by the DFS solver.

## Package structure

```text
mazegen/
├── __init__.py
├── algorithm/
│   ├── base.py
│   ├── huntkill.py
│   ├── recursive_backtracker.py
│   └── prim.py
├── model/
│   ├── cell.py
│   ├── constants.py
│   ├── maze.py
│   └── maze_generator.py
├── pattern/
│   ├── forty_two.py
│   └── utils.py
└── solver/
    ├── base.py
    ├── bfs.py
    ├── dfs.py
    └── astar.py
```

## Extending `mazegen`

Generation and solving logic use the Strategy pattern. New algorithms can be added without changing the maze model.

### Adding a generation algorithm

Create a class inheriting from `MazeAlgorithmStrategy` and implement `generate_algorithm(generator, maze)`.
Then add its value to `MazeAlgorithm` and register the strategy in the algorithm map used by `get_algorithm()`.

```python
from .base import MazeAlgorithmStrategy


class NewAlgorithm(MazeAlgorithmStrategy):
    def __init__(self) -> None:
        super().__init__("New Algorithm")

    def generate_algorithm(self, generator, maze) -> None:
        # generation logic
        pass
```

### Adding a solver

Create a class inheriting from `MazeSolutionStrategy` and implement `generate_solution(maze)`.
Then add its value to `SolutionAlgorithm` and register it in the map used by `get_solution_algorithm()`.

```python
from .base import MazeSolutionStrategy


class NewSolver(MazeSolutionStrategy):
    def __init__(self) -> None:
        super().__init__("New Solver")

    def generate_solution(self, maze):
        # solving logic
        pass
```

Keeping new strategies dependent on the public `Maze` methods preserves the separation between maze structure, algorithms, and external visualization.
