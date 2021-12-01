#!/usr/bin/python3

import time
import re
import itertools


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


# def invert_zeroes_and_ones(zeroes_and_ones: str):
#     res = zeroes_and_ones
#     res = res.replace("1", "x")
#     res = res.replace("0", "1")
#     res = res.replace("x", "0")
#     return res


def reverse_order(zeroes_and_ones: str):
    # tested OK
    res = ""
    for i in range(10):
        res += zeroes_and_ones[9-i]
    return res


class Tile:
    id = 0
    edges = list()   # 4 values for N,S,E,W edges
    reversed_edges = list()   # 4 values for N,S,E,W edges
    matching = list()
    matching_indexes = list()
    data = list()

    def calculate_edges(self):
        v_top = ""
        v_bottom = ""
        v_left = ""
        v_right = ""
        for i in range(10):
            # TOP = 9to0
            if self.data[0][9-i] == "#":
                v_top += "1"
            else:
                v_top += "0"
            # RIGHT = 0to9
            if self.data[i][9] == "#":
                v_right += "1"
            else:
                v_right += "0"
            # BOTTOM = 0to9
            if self.data[9][i] == "#":
                v_bottom += "1"
            else:
                v_bottom += "0"
            # LEFT = 9to0
            if self.data[9-i][0] == "#":
                v_left += "1"
            else:
                v_left += "0"
        self.edges = list()
        self.edges.append(int(v_top, 2))
        self.edges.append(int(v_bottom, 2))
        self.edges.append(int(v_left, 2))
        self.edges.append(int(v_right, 2))
        self.reversed_edges = list()
        self.reversed_edges.append(int(reverse_order(v_top), 2))
        self.reversed_edges.append(int(reverse_order(v_bottom), 2))
        self.reversed_edges.append(int(reverse_order(v_left), 2))
        self.reversed_edges.append(int(reverse_order(v_right), 2))


    def rotate_left(self):
        rows = list()
        for j in range(10):
            cols = list()
            for i in range(10):
                cols.append(self.data[i][9-j])
            rows.append(cols)
        self.data = rows
        self.calculate_edges()
        return self



def read_file(filename):
    res = dict()
    nb_lines = 0
    f = open(filename, 'r')
    lines = f.readlines()
    cur_tile = Tile()
    for line in lines:
        text = line.strip()
        if len(text) == 0:
            # empty line
            nb_lines += 0
        else:
            # data line
            data = text.strip()
            match = re.match(r'^Tile ([0-9]+):$', data)
            if match is not None:
                # Tile 2311:
                cur_tile = Tile()
                cur_tile.id = int(match.groups()[0])
                cur_tile.edges = list()
                cur_tile.data = list()
                res[cur_tile.id] = cur_tile
            else:
                # ..##.#..#.
                cur_tile.data.append(list(data))  # list cuts string into list of chars
    for t in res.values():
        t.calculate_edges()
    return res


# regex_examples()
# print(combinations(["A", "B", "C"], range(2,3)))
# print(combinations(["X", "Y", "Z"]))

tiles = read_file('input.txt')

tot = 0
for tile in tiles.values():
    #print("{} => {}".format(tile.id, tile.edges))
    nb_match = 0
    tile.matching = list()
    tile.matching_indexes = list()
    for t2 in tiles.values():
        if t2 != tile:
            # compare borders
            idx = -1
            for val in tile.edges:
                idx += 1
                for v2 in t2.edges:
                    if val == v2:
                        # matching borders
                        nb_match += 1
                        tile.matching.append(t2.id)
                        tile.matching_indexes.append(idx)
                for v2 in t2.reversed_edges:
                    if val == v2:
                        # matching borders
                        tile.matching.append(t2.id)
                        tile.matching_indexes.append(idx)
                        nb_match += 1
    if nb_match == 2:
        print("{} => {} matching borders".format(tile.id, nb_match))

print("number of lines {}".format(len(tiles.keys())))

# PART1
print(3833 * 2593 * 2999 * 3517)


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


def find_right_tile(tile: Tile, remaining: dict):
    for test in remaining.values():
        for i in range(4):
            test.rotate_left()
            if tile.edges[3] == test.reversed_edges[2]:
                return test


# Recompose image
remaining = tiles.copy()
start = remaining[3833]  # corners 3833  2593  2999  3517)

print("Start from {}".format(start.matching))

tile = start
ligne = list()
ligne.append(tile)
remaining = removekey(remaining, tile.id)

next_tile = find_right_tile(tile, remaining)
if next_tile is not None:
    remaining = removekey(remaining, next_tile.id)
    ligne.append(next_tile)

# Draw picture
for j in range(10):
    for item in ligne:
        for i in range(10):
            print("{} ".format(item.data[j][i]), end="")
        print(" - ", end="")
    print("")


print("{} / {}".format(start.matching, start.matching_indexes))

