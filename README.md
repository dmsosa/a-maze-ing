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

#  Render part
Key Characters for ASCII Mazes
Common characters used to represent maze elements include:

Walls: #, █, ■
Paths: , ., .
Start/End: S, E, *
Corners: +, ┌, ┐, └, ┘ 


# Resources

Python Packaging User Guide: https://packaging.python.org/en/latest/tutorials/packaging-projects/

Printing mazes with Ascii

https://codereview.stackexchange.com/questions/263517/more-efficient-way-to-create-an-ascii-maze-using-box-characters

Print a maze using only two characters
https://stackoverflow.com/questions/55452329/print-a-maze-using-only-two-characters

# ToDo

Move config logic outside mazegen package
Add santi to authors
Mazegen needs to be built first.
Makefile debug rule.
Makefile test to run tests


# Rendering the maze 
Create maze renderer with ascii characters only
If I decide to take into account both 4 sides, I need to have 

.=.=======.
| |       |
|     .=. |
|     | | |
.=====| 
|     
.=========.

**********
|  |  *     *
└──┘  *  *
*E *  *  *
* S*  *  *
*     *  *
**********


// Source - https://codereview.stackexchange.com/a/263520
// Posted by Olivier Jacot-Descombes, modified by community. See post 'Timeline' for change history
// Retrieved 2026-09-05, License - CC BY-SA 4.0

char[] walls = {
//   0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15
    '*', '─', '│', '┌', '│', '└', '│', '├', '─', '─', '┐', '┬', '┘', '┴', '┤', '┼' 
};

int index = (curNorth ? 1 : 0) + 
            (curWest ? 2 : 0) + 
            (nextEast ? 4 : 0) + 
            (nextSouth ? 8 : 0);
char corner = walls[index];



[┌][─][┐]
[|][*][|]
[└][─][┘]
[┌][─][┐]
[|][*][|]
[└][─][┘]
[┌][─][┐]
[|][*][|]
[└][─][┘]
[┌][─][┐]
[|][*][|]
[└][─][┘]
[┌][─][┐]
[|][*][|]
[└][─][┘]
[┌][─][┐]
[|][*][|]
[└][─][┘]

then displays the grid once is built is easy
for y in height
    i = 0
    for x in width
        j = 0
        while j < cellSize
            row += grid[y*i][x+j]
            i++
            j++

For box-drawing characters (─ │ ┌ ┐ ┬ ┼ etc.) instead, see the related Code Review thread, which uses a 4-bit lookup table to pick the correct corner/junction character.

maybe I need to take care of the four corners?
or only one corner.

# EventEmitter pattern:


Good call, actually — decoupling the renderer from Cell/Direction/Maze internals and pinning it to one stable contract (list[str] of hex rows) means you could swap MazeGenerator's internal cell representation entirely later without touching the renderer at all. Since Maze.digits is already a @property computed fresh from cells each time, emitting it on every "cell_updated" event costs you nothing extra architecturally — it's just generator.digits read at call time, no new generator method needed.


# Exception Handling

Why this works
Signal	What happens	Where it's caught
Ctrl+C during input()	input() raises KeyboardInterrupt	Inner try/except
Ctrl+C during processing	Propagates up	Outer try/except
Ctrl+D during input()	input() raises EOFError	Inner try/except
Piped input ends (e.g. cat file | python3 prog.py)	Also EOFError	Same place

Key practices
Catch KeyboardInterrupt and EOFError together around input() — they both mean "stop reading."
Use exit code 130 for Ctrl+C (128 + SIGINT(2)), 0 for clean exit, 1 for errors. This is the Unix convention.
Don't catch KeyboardInterrupt silently — at minimum print a message so the user knows the program didn't crash.
Keep the outer try/except as a safety net for interrupts that fire between prompts (during your processing logic).
Avoid signal.signal for simple input programs — the try/except approach is simpler and handles the common case perfectly. Reserve the signal-flag pattern for long-running servers or multi-threaded apps where you need graceful shutdown of resources (DB pools, sockets, etc.).
This two-layer try/except is the idiomatic, minimal solution for input-driven CLI programs.

# To Do

Handle uncomplete config.txt file, by providing default values, what else could I do to handle missing configuration?
could be cool to indicate the user which fields are missing, and then informing that we are using default values.


    I NEED TO MAKE THE CONFIG ABLE TO RECEIVE CONFIG FILE NAMES WITHOUT BEING LOWERCASE. 
    ALSO, I WANT TO MAKE THE INTERACTIVE MENU, OPTIONS ARE 
    CHANGE CONFIGURATION , SHOWS CURRENT CONFIG OBJECT AND ALLOWS TO CHANGE THEIR VALUES 
    3. GENERATE NEW MAZE 
    2. SHOW AND HIDE SOLUTION , CHANGE THEME 
    1. FOR INT FIELDS, CHECK IF THEY ARE ALSO NOT BOOLENS 
    5. I NEED TO handle permission errors and errors related to file management 
    Add number of stepts that the maze make,
    put a chronometer
    put the number of steps made by the user

    // 14 sept
    as for today, the program depends on play manager while loop, now, it can provide an option for navigating through functions, it has the function edit maze configuration, which is going to edit fields over the config object, initialize a new maze generator cleaning the previous one, and re generate the maze.

    when the user presses enter, I need to move the cursor where the menu begins, print the configuration menu, how to pad the configuration menus to the same height?

    while editing config, handle key up and down to be able to switch opitions, for that reason

    for that you use the Menu class for access rthe selected option, and when you press enter, you call a function

    IN OR
    // 15 sept
    as for today
    the program needs to show the solution, once I ave the solution, i can show it  via the state mask array, but when I want the

    SHOWING THE SOLUTION:
    WHERE: IN THE MAZE GENERATOR object
    WHEN: when the boolean value render.show_solution is True, or whether my render receives an optional array of tuples that is the solution. 
    WHERE the solution is? It is found by the MazeSolver class, which takes an entry, an exit, the representation in hexadecimal digits
    then the array with solution is going to be provided by the maze generator ALWAYS receives


    the program now renders a maze but I need to make it able to enter into a while loop after displaying an options menu.

    SO, NOW THAT THE SOLUTIONS EXIST, CAN I CHANGE THE PASSING INFO AROUND TO BE ABLE TO JUST UPDATE THE RENDER DETAILS IN THE EVENT THAT IS BEING EMITTED,



    IF NOT, CAN I JUST GRAB SOLUTIONS FROM THE INFO? LETS TRY
    THAT event is going to be fired from the solver. I want to get the solution once I discover it and save it for later, so that it can be printed only by setting the show_solution flag to true, and making the play_manager to re render it.




    Now, how the play manager is going to display a good menu? lest ask claude code.

    It should be like

    for item in menu.items.
    print [index item.key] - label
    if key == item.key call play_manager._generate_new_maze() 

    # BONUS
    add benchmark to the maze as it is being generated, which comes above the menu


    REDIRECT EXIT TO WIDHT -1 HEIGHT -1
    FIX THE MENU IN ASCII MODE
    PRINT EXIT AND ENTRY ALWAYS
    LET THE MAZE DO NOT OVERRIDE SOLUTION OVER PLAY, ENTRY AND EXIT
    
    need to block boolean to change width and height 
    need to provide a way to change theme chars and colors 

    need to make it playable 
    
    reduce limits to height and width

