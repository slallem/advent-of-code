
# Array of String [ ['hello'], ['world'] ]
def read_file_lines(file, ignore_empty=True):
    res = []
    f = open('input.txt', 'r')
    lines = f.readlines()
    for line in lines:
        text = line.strip()
        if (not ignore_empty) or (len(text) > 0):
            res.append(text)
    return res


# Array of Array of Char [ ['h','e','l','l','o'], ['w','o','r','l','d'] ]
def read_file_chars(file, ignore_empty=True):
    res = []
    lines = read_file_lines(file, ignore_empty)
    for line in lines:
        res.append(list(line))
    return res


terrain = read_file_chars('input.txt')


def slope(xx, yy):
    nb_moves = 0
    nb_dots = 0
    nb_trees = 0
    x = 0
    y = 0
    last_line = len(terrain)-1
    while True:
        y += yy
        line_length = len(terrain[y])
        if line_length > 0:
            nb_moves += 1
            x += xx
            car = terrain[y][(x % line_length)]
            # print(len(chars), end="")
            # print(car, end="")
            if car == '#':
                nb_trees += 1
            elif car == '.':
                nb_dots += 1
            # else:
            # print(">>>{}<<<".format(car))
            if y >= last_line:
                break

    print("slope for x {} y {} moves {} dots {} trees {} total {}".format(xx, yy, nb_moves, nb_dots, nb_trees, nb_dots+nb_trees))
    return nb_trees


# Part #1
slope(3, 1)

# Part #2
print()
print(slope(1, 1) * slope(3, 1) * slope(5, 1) * slope(7, 1) * slope(1, 2))
