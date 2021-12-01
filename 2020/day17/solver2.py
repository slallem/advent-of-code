#!/usr/bin/python

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
    print(re.match(r'^([ a-z0-9^:]+):.([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)$', "departure date: 41-532 or 552-956").groups())


def combinations(items: list, r: range = None):
    c = list()
    if r is None:
        r = range(1, len(items)+1)
    for i in r:
        c.extend(list(itertools.combinations(items, i)))
    return c


def decode_ligne(data):
    res = list(data)
    #print("data {}".format(chars))
    return res


def read_file(filename):
    res = list()
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
            res.append(decode_ligne(data))
    return res


start = time.time()

# regex_examples()
# print(combinations(["A", "B", "C"], range(2,3)))
# print(combinations(["X", "Y", "Z"]))

lines = read_file('input.txt')

print("number of lines {}".format(len(lines)))

neighbours3d = [
    [-1, -1, -1], [0, -1, -1], [1, -1, -1],
    [-1,  0, -1], [0,  0, -1], [1,  0, -1],
    [-1,  1, -1], [0,  1, -1], [1,  1, -1],
    [-1, -1,  0], [0, -1,  0], [1, -1,  0],
    [-1,  0,  0], [0,  0,  0], [1,  0,  0],
    [-1,  1,  0], [0,  1,  0], [1,  1,  0],
    [-1, -1,  1], [0, -1,  1], [1, -1,  1],
    [-1,  0,  1], [0,  0,  1], [1,  0,  1],
    [-1,  1,  1], [0,  1,  1], [1,  1,  1],
]

neighbours = list()
for zz4 in range(-1, 2):
    for n in neighbours3d:
        e = n.copy()
        e.append(zz4)
        neighbours.append(e)

neighbours.remove([0, 0, 0, 0])

map2d = [
    "..#..#.#",
    "##.#..#.",
    "#....#..",
    ".#..####",
    ".....#..",
    "...##...",
    ".#.##..#",
    ".#.#.#.#"
]
#
# map2d = [
#     ".#.",
#     "..#",
#     "###"
# ]
#

def make_key(x: int, y: int, z: int, z4: int):
    #return "{},{},{},{}".format(x, y, z, z4)
    return x + y*1000 + z*1000000 + z4*1000000000


def is_active(dim: set, x: int, y: int, z: int, z4: int):
    position = make_key(x, y, z, z4)
    return position in dim


def set_active(dim: set, x: int, y: int, z: int, z4: int, value: bool):
    position = make_key(x, y, z, z4)
    #print("* setting {} to {}".format(position, value))
    if value:
        dim.add(position)
    else:
        if position in dim:
            dim.remove(position)


def count_active_neighbours(dim: set, x: int, y: int, z: int, z4: int):
    res = 0
    for n in neighbours:
        if is_active(dim, x + n[0], y + n[1], z + n[2], z4 + n[3]):
            res += 1
    return res


# def print_dim(dim: set, width: int = 3):
#     max_dim = int(width/2)
#     rx = range(-max_dim, max_dim+1)
#     ry = range(-max_dim, max_dim+1)
#     rz = range(-max_dim, max_dim+1)
#     for k in rz:
#         print("z={}".format(k))
#         for j in ry:
#             for i in rx:
#                 if is_active(dim, i, j, k):
#                     print("#", end="")
#                 else:
#                     print(".", end="")
#             print("")
#         print("")
#     print("")


def do_a_cycle(dim: set):
    orig = copy.deepcopy(dim)
    # orig = dim
    max_dim = 9
    nbleftactive = 0
    rx = range(-max_dim, max_dim)
    ry = range(-max_dim, max_dim)
    rz = range(-max_dim, max_dim)
    rz4 = range(-max_dim, max_dim)
    for k4 in rz4:
        for k in rz:
            for j in ry:
                for i in rx:
                    # - If a cube is active and exactly 2 or 3 of its neighbors are also active,
                    # the cube remains active. Otherwise, the cube becomes inactive.
                    # - If a cube is inactive but exactly 3 of its neighbors are active,
                    # the cube becomes active. Otherwise, the cube remains inactive.
                    nb_active_neighbours = count_active_neighbours(orig, i, j, k, k4)
                    if is_active(orig, i, j, k, k4):
                        # Cube is active
                        if nb_active_neighbours == 2 or nb_active_neighbours == 3:
                            nbleftactive += 1
                            pass  # stays active
                        else:
                            set_active(dim, i, j, k, k4, False)
                    else:  # Cube is NOT active
                        if nb_active_neighbours == 3:
                            set_active(dim, i, j, k, k4, True)
                        else:
                            pass  # stays inactive
    return nbleftactive

# Initialization of dim3d


dim3d = set()
w = len(map2d[0])
h = len(map2d)
ofs = int(w/2)
print("w {} h {} ofs {} range {}".format(w, h, ofs, range(-ofs, ofs+1)))
for zz4 in range(0, 1):
    for zz in range(0, 1):
        jj = 0
        for yy in range(-ofs, -ofs+w):
            row = list(map2d[jj])
            print("row {}".format(row))
            jj += 1
            ii = 0
            for xx in range(-ofs, -ofs+w):
                char = row[ii]
                ii += 1
                set_active(dim3d, xx, yy, zz, zz4, (char == "#"))


print("Init = {}".format(len(dim3d)))
print("  dim3d {}".format(dim3d))
#print_dim(dim3d, 3)
print()

for loop in range(6):
    val = do_a_cycle(dim3d)
    print("Cycle {} = {} leftactive {}".format(loop + 1, len(dim3d), val))
    #print_dim(dim3d, 5)
    print()


end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))

# fin partie 2 à 8h03
# Difficultés de cet exercice : beaucoup de temps perdu a cause de l'initialisation qui se faisait mal
# Mal lu l'énoncé ; j'avais initialisé à tort la map3d avec un cube (N x N x N) fait à partir du (N x N) ...
# Il suffisait juste d'initialiser la map2d donnée sur le plan XY de notre espace XYZ ... grr
