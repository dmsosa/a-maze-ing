# Developer's Forewords:

In computer science, maze generation is more than just fun: it’s a practical
application of algorithms, randomness, and graph theory. Some famous algorithms used
for maze generation, like Prim’s, Kruskal’s, or the recursive backtracker, are also used in
real-world problems like network design or procedural content generation. Interestingly,
perfect mazes (with one unique path between any two points) are directly related to
spanning trees in graph theory. Building a maze, especially one you can visualize and
share, is a great way to explore how computers can create structure from chaos, and have
a bit of fun while doing it.
“A labyrinth is not a place to be lost, but a path to be found.”

# Learning path

# Packaging a Python project

The directory containing the Python files should match the project name. This simplifies the configuration and is more obvious to users who install the package.

Creating the file __init__.py is recommended because the existence of an __init__.py file allows users to import the directory as a regular package, even if (as is the case in this tutorial) __init__.py is empty. [1]


Starting a mazze ing

the first question is the algorithm I am going to choose, for that, I am going to use the DFS algorithm but with the Hunt and kill variant which avoids using recursion.

But, how to implement that algorithm with the parse part. Which classes I am going to create? for example, how can I process that config file. 

From the config.txt, the main goal is to take out variables out of that, how can I read that file?

If you pass me the file as a command line argument, I can open it, otherwise, I am going to look for a config.txt file, in which case if not found, I throw an exception

but, how I am going to manae the dependdencies of my project, should I use a requirements.txt or a poetry, ?

# The flow of the program:

My first idea is: I receive a config.txt file, 
whicih is going to be parsed by MazeConfiguration class in order to create a MazeConfiguration object via its init method. After parsing it I can initialize my MazeGenerator class using the properties that my maze_config has.

My main function is where? it is going to be in the a_maze_ing.py file. Which checks how many arguments you pass me, tries to find config.txt if not found, and throw error if no file was found.

The first challenge: read 
https://medium.com/@msgold/using-python-to-create-and-solve-mazes-672285723c96

and develop a program that starts at cell Entry, access a random neighbour and print its coordinates, recursively.

you are allowed to pass the subject AI to explain it in other words

write pyttest for unit testing

Your program must handle all errors gracefully: invalid configuration, file not found, bad
syntax, impossible maze parameters, etc. It must never crash unexpectedly, and must
always provide a clear error message to the user.

this stuff is going to implement the Eller's Agorithm to generate the maze.
then, we take care of printing the maze itself.


For me, it makes sense to create a pre Configuration class? It may allow me to create a Maze rather than dealing with config error identifications inside the Maze class itself, and then the Maze Generator class creation can be pretty straightforward.



# Resources

Python Packaging User Guide: https://packaging.python.org/en/latest/tutorials/packaging-projects/
# ToDo

Move config logic outside mazegen package
Add santi to authors
Mazegen needs to be built first.
Makefile debug rule.
Makefile test to run tests.