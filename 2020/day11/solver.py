
import time
import re
import itertools
import copy

def regex_examples():
    sample = 'les années 1950 à 2000 couvrent 50 années de fooooolie'
    print(re.findall(r'([0-9]+)', sample))
    print(re.findall(r'(ANN)', sample, re.IGNORECASE))
    print(re.findall(r'(xyz)', sample))
    print(re.match(r'^(.+95)', sample) is not None)
    print(re.match(r'xyz', sample) is not None)


def minval(arr):
    res = arr[0]
    for val in arr:
        if val < res:
            res = val
    return res


def maxval(arr):
    res = arr[0]
    for val in arr:
        if val > res:
            res = val
    return res


def combinations(items: list, r: range = None):
    c = list()
    if r is None:
        r = range(1, len(items)+1)
    for i in r:
        c.extend(list(itertools.combinations(items, i)))
    return c


def decode_ligne(data):
    chars = list(data)
    #print("data {}".format(chars))
    return chars


def read_file(filename):
    carte = list()
    nb_lines = 0
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        text = line.strip()
        if len(text) == 0:
            # empty line
            nb_lines += 0
        else:
            # data line
            data = text.strip()
            nb_lines += 1
            carte.append(decode_ligne(data))
    #print("number of lines {}".format(nb_lines))
    return carte


def get_char_at(grid, x, y):
    if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
        return "."
    return grid[y][x]


def is_seat(grid, x, y):
    return get_char_at(grid, x, y) != "."


def count_adjacent_occupied(grid, x, y):
    res = 0
    if get_char_at(grid, x-1, y-1) == "#":
        res += 1
    if get_char_at(grid, x-1, y) == "#":
        res += 1
    if get_char_at(grid, x-1, y+1) == "#":
        res += 1
    if get_char_at(grid, x, y-1) == "#":
        res += 1
    if get_char_at(grid, x, y+1) == "#":
        res += 1
    if get_char_at(grid, x+1, y-1) == "#":
        res += 1
    if get_char_at(grid, x+1, y) == "#":
        res += 1
    if get_char_at(grid, x+1, y+1) == "#":
        res += 1
    return res


def apply_rules(grid: list):
    res = 0
    original = copy.deepcopy(grid)
    for j in range(len(original)):
        for i in range(len(original[0])):
            # rules
            char = get_char_at(original, i, j)
            # rule 1
            if char == 'L':  # free seat
                if count_adjacent_occupied(original, i, j) == 0:
                    grid[j][i] = "#"
                    res += 1
            #rule2
            elif char == '#':  # occupied seat
                res += 1
                if count_adjacent_occupied(original, i, j) >= 4:
                    grid[j][i] = "L"
                    res -= 1
    return res


def print_grid(grid):
    for line in grid:
        for char in line:
            print(char, end="")
        print("", flush=True)


start = time.time()

# regex_examples()
# print(combinations(["A", "B", "C"], range(2,3)))
# print(combinations(["X", "Y", "Z"]))
layout = read_file('input.txt')

nb_cols = len(layout[0])
nb_rows = len(layout)

iter = 0
last_val = -1
while True:
    iter += 1
    print("iteration {} : ".format(iter), end="", flush=True)
    occupied = apply_rules(layout)
    if last_val != occupied:
        last_val = occupied  # seats changed
        print("seats changed, now is {}".format(occupied))
    else:
        #unchanged
        print("seats UNCHANGED, still {}".format(occupied))
        break
    if iter < 3:
        print_grid(layout)
    print("")



end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))