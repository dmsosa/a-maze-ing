# Implementing the parsing of config. txt

example config.txt

If I split the config with =, you can troll me easily because I get an array like

[WIDTH, 3, HEIGHT, 5, '', '', 'RandomStuff', '@€']

Not good, if I split by newlines, I can get each line of the config file, If I get an empty line I decide if throw an error or not, for now I am just going to ignore it. So:

