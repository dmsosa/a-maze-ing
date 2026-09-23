# mazegen

`mazegen` is a Python package for generating, solving, and exporting mazes.

It separates maze representation, generation algorithms, solving algorithms, and additional maze features into independent components.

## Structure

```text
mazegen/
├── __init__.py
│
├── algorithm/
│   ├── __init__.py
│   ├── base.py
│   ├── huntkill.py
│   ├── recursive_backtracker.py
│   └── prim.py
│
├── solver/
│   ├── __init__.py
│   ├── base.py
│   ├── bfs.py
│   ├── dfs.py
│   └── astar.py
│
├── model/
│   ├── __init__.py
│   ├── cell.py
│   ├── constants.py
│   ├── maze.py
│   └── maze_generator.py
│
├── pattern/
│   ├── __init__.py
│   ├── forty_two.py
│   └── utils.py
│
└── exception/
    ├── __init__.py
    └── maze_exception.py
```

## Architecture overview

```text
MazeGenerator
      │
      ├── creates ──→ Maze
      │
      ├── uses ─────→ Generation Strategy
      │
      ├── uses ─────→ Solution Strategy
      │
      └── exports ──→ Output
```

The package is built around a clear separation of responsibilities:

| Component       | Responsibility                                     |
| --------------- | -------------------------------------------------- |
| `Cell`          | Represents a single maze cell and its walls.       |
| `Maze`          | Stores and modifies the maze structure.            |
| `MazeGenerator` | Coordinates maze generation and solving.           |
| `algorithm`     | Contains maze generation strategies.               |
| `solver`        | Contains maze solving strategies.                  |
| `pattern`       | Defines and positions blocked maze patterns.       |
| `constants`     | Defines available algorithms and shared constants. |
| `exception`     | Contains maze-specific exceptions.                 |

## Quick usage

```python
from mazegen import MazeGenerator, MazeAlgorithm, SolutionAlgorithm

generator = MazeGenerator(
    width=20,
    height=20,
    entry=(0, 0),
    exit=(19, 19),
    algorithm=MazeAlgorithm.PRIM,
    solution_algorithm=SolutionAlgorithm.ASTAR,
    seed=42,
    perfect=True,
)

maze = generator.generate()

generator.export_maze()
```

## Core components

### `Cell`

Represents a single maze cell, including its coordinates, walls, and blocked state.

| Method                | Description                                               |
| --------------------- | --------------------------------------------------------- |
| `has_wall(direction)` | Checks for a wall in the specified direction.             |
| `ctoh()`              | Returns the hexadecimal representation of the cell walls. |

### `Maze`

Stores and modifies the complete maze structure.

| Method                          | Description                                      |
| ------------------------------- | ------------------------------------------------ |
| `get_cell(x, y)`                | Returns the cell at the given coordinates.       |
| `get_neighbors(x, y)`           | Returns adjacent cells.                          |
| `get_available_neighbors(x, y)` | Returns adjacent cells available for generation. |
| `get_open_neighbors(x, y)`      | Returns cells connected by an open passage.      |
| `remove_wall(x, y, direction)`  | Opens a passage between adjacent cells.          |
| `block_cells(positions)`        | Marks cells as blocked.                          |

Generation and solving strategies should interact with the maze through its public methods instead of modifying the internal cell matrix directly.

### `MazeGenerator`

Coordinates the complete maze creation process.

```text
Initialize Maze
      ↓
Apply Pattern
      ↓
Generate Maze
      ↓
Add Loops (optional)
      ↓
Solve Maze
      ↓
Return Maze
```

Main methods:

| Method             | Description                          |
| ------------------ | ------------------------------------ |
| `generate()`       | Generates and solves the maze.       |
| `make_imperfect()` | Adds extra passages to create loops. |
| `output_text()`    | Creates the output representation.   |
| `export_maze()`    | Writes the maze output to a file.    |

## Generation algorithms

Generation algorithms inherit from `MazeAlgorithmStrategy`.

| Algorithm             | Description                                                                  |
| --------------------- | ---------------------------------------------------------------------------- |
| Hunt and Kill         | Alternates between random exploration and searching for new unvisited cells. |
| Recursive Backtracker | Uses depth-first exploration and backtracking.                               |
| Randomized Prim       | Expands the maze through randomly selected frontier cells.                   |

They mainly interact with:

```python
maze.get_cell()
maze.get_available_neighbors()
maze.remove_wall()
```

The strategy decides which cells should be connected, while `Maze` performs the structural changes.

## Solving algorithms

Solvers inherit from `MazeSolutionStrategy`.

| Algorithm | Description                                                    |
| --------- | -------------------------------------------------------------- |
| BFS       | Explores level by level and finds a shortest path.             |
| DFS       | Explores one branch deeply before backtracking.                |
| A*        | Uses movement cost and Manhattan distance to guide the search. |

Solvers mainly navigate the maze through:

```python
maze.get_open_neighbors()
```

## Features

### Perfect and imperfect mazes

A perfect maze contains exactly one path between any two accessible cells.

Setting:

```python
perfect=False
```

allows additional passages to be opened after generation, creating loops.

### 42 pattern

The `pattern` package defines the blocked cells used to create the centered `42` shape.

Generation algorithms automatically ignore blocked cells.

### Events

`MazeGenerator` can emit events during generation, allowing renderers or other components to observe the process without being coupled to the generation algorithms.

```python
generator.on(event, callback)
generator.off(event, callback)
```

### Export

The generated output contains:

```text
hexadecimal maze
entry coordinates
exit coordinates
solution path
```

## Extending mazegen

Generation and solving algorithms use the Strategy pattern.

New strategies should depend on the public `Maze` interface instead of accessing or modifying its internal cell storage directly.

### Adding a generation algorithm

Create a class inheriting from:

```python
MazeAlgorithmStrategy
```

and implement:

```python
generate_algorithm(generator, maze)
```

Then:

1. Add the algorithm to `MazeAlgorithm`.
2. Register it in `ALGORITHM_MAP`.
3. Implement the generation logic using the public `Maze` methods.

Example:

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

Create a class inheriting from:

```python
MazeSolutionStrategy
```

and implement:

```python
generate_solution(maze)
```

Then:

1. Add the solver to `SolutionAlgorithm`.
2. Register it in `SOLUTION_ALGORITHM_MAP`.
3. Implement the solving logic using the public `Maze` interface.

Example:

```python
from .base import MazeSolutionStrategy


class NewSolver(MazeSolutionStrategy):

    def __init__(self) -> None:
        super().__init__("New Solver")

    def generate_solution(self, maze):
        # solving logic
        pass
```
