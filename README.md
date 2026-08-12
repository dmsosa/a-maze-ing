Starting a mazze ing

the first question is the algorithm I am going to choose, for that, I am going to use the DFS algorithm but with the Hunt and kill variant which avoids using recursion.

But, how to implement that algorithm with the parse part. Which classes I am going to create? for example, how can I process that config file. 

From the config.txt, the main goal is to take out variables out of that, how can I read that file?

If you pass me the file as a command line argument, I can open it, otherwise, I am going to look for a config.txt file, in which case if not found, I throw an exception

but, how I am going to manae the dependdencies of my project, should I use a requirements.txt or a poetry, ?

# The flow of the program:

My first idea is: I receive a config.txt file, after parsing it I can initialize my MazeGenerator class.
My main function is where? it is going to be in the a_maze_ing.py file. Which checks how many arguments you pass me, tries to find config.txt if not found, and throw error if no file was found.

The first challenge: read 
https://medium.com/@msgold/using-python-to-create-and-solve-mazes-672285723c96

and develop a program that starts at cell Entry, access a random neighbour and print its coordinates, recursively.

you are allowed to pass the subject AI to explain it in other words

write pyttest for unit testing

Your program must handle all errors gracefully: invalid configuration, file not found, bad
syntax, impossible maze parameters, etc. It must never crash unexpectedly, and must
always provide a clear error message to the user.