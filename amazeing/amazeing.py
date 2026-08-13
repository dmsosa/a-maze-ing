def parse_config(config_content: str):
    conf = config_content.split("\n")
    info = {}
# iterate over each line, detect width, height, flag, if found an unknown flag throw error, I am going to split each line by =, where the index 0 is expected to be the key (must be a valid key) and the index [1] must be the value which is going to be validated depending on which key it is related to. Now, if the len of the split by "=" is different than 2, throw error because of bad parsing on line (line_count), can I tell which column failed by parsing?
    line_count = 1 
    for (line in conf_lines):
        line_split = conf_lines.split("=")
        if (len(line_split) != 2)
            raise Exception("")
        key, value = line_split
        if (key.upper() == "WIDTH")
            if key.upper() != key
                raise Exception
            try:
                info[key] == int(value)

            except Exception as e:
                raise Exception("Width value is not valid: e.message")
       return (info)

if __name__ == "__main__":
    arglen = len(sys.argv)
    if (arglen < 2):
        print("Correct usage must be: a_maze_ing.py <configfile>")
        sys.exit(1)
    maze_info = ""
    try:
        with (open(sys.argv[1], 'r') as f:):
        config_content = f.read()
        maze_info = parse_config(config_content)   
    except FileNotFoundException:
           print("File not found")
    except Exception as e:
           print(f"{e}")
    maze = MazeGenerator(info)
    print_maze_beauty()
#how do I  generate that fancy animation of the maze being created?
    update_char_pos()
#how do I re-print the maze unnoticablz so that I make the ilusion of movement?
    print_maze()

def update_char_pos(from: Cell, to: Cell)
    maze.setCell(to.x, to.y, from.value)
    maze.setCell(from.x, from.y, EMPTY)
    