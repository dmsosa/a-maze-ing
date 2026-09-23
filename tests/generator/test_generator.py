from mazegen.model.constants import MazeAlgorithm
from mazegen.model.maze_generator import MazeGenerator
from mazegen.export import output_text, export_maze
from mazegen.solver import solve_bfs


generator = MazeGenerator(
    width=5,
    height=5,
    entry=(0, 0),
    exit=(4, 4),
    algorithm=MazeAlgorithm.HUNT_AND_KILL,
    seed=42,
)

maze = generator.generate()

print("Maze generated")
print("Rows:", len(maze.cells))
print("Columns:", len(maze.cells[0]))

solution = solve_bfs(maze)

print()
print("Export format:")
print(output_text(maze, solution))


def validate_solution(maze, solution):
    x, y = maze.entry

    for move in solution:
        valid_move = False

        for direction, neighbor in maze.get_open_neighbors(x, y):
            if direction.name == move:
                x = neighbor.x
                y = neighbor.y
                valid_move = True
                break

        if not valid_move:
            return False

    return (x, y) == maze.exit


print()
print("Solution valid:", validate_solution(maze, solution))

export_maze(
    maze,
    solution,
    "output.txt",
)
