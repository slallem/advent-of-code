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


def flip(tiles: set, position: int):
    print("Flipping {}".format(position))
    if position in tiles:
        tiles.remove(position)
    else:
        tiles.add(position)


def decode_ligne(data):
    res = data
    res = res.replace("nw", "x")
    res = res.replace("sw", "y")
    res = res.replace("ne", "f")
    res = res.replace("se", "g")
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

gw = 10000
floor = set()

curpos = int(gw/2) * gw + int(gw/2)
curpos = 0
for line in lines:
    newpos = curpos
    for char in list(line):
        if char == 'w':
            newpos -= 1
        elif char == 'e':
            newpos += 1
        elif char == 'x':
            newpos -= (gw+1)
        elif char == 'y':
            newpos += gw
        elif char == 'f':
            newpos -= gw
        elif char == 'g':
            newpos += (gw+1)
        else:
            print(line)
            raise Exception("unexpected char {}".format(char))
    flip(floor, newpos)



print(floor)
print()
print(len(floor))


def white(tiles: set, flipped: set, pos: int):
    #Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
    if pos in tiles:
        return  # ony test white tiles
    nb = 0
    if pos-gw in tiles:
        nb += 1
    if pos-(gw+1) in tiles:
        nb += 1
    if pos+gw in tiles:
        nb += 1
    if pos+(gw+1) in tiles:
        nb += 1
    if pos-1 in tiles:
        nb += 1
    if pos+1 in tiles:
        nb += 1
    if nb == 2:
        flipped.add(pos)



for day in range(100):
    yesterday = floor.copy()
    toremove = set()
    toadd = set()
    for idx in floor:  # black tiles
        cnt = 0
        if idx-gw in floor:
            cnt += 1
        if idx-(gw+1) in floor:
            cnt += 1
        if idx+gw in floor:
            cnt += 1
        if idx+(gw+1) in floor:
            cnt += 1
        if idx-1 in floor:
            cnt += 1
        if idx+1 in floor:
            cnt += 1
        #Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
        if cnt == 0 or cnt > 2:
            toremove.add(idx)
    #print("floor before {}".format(floor))
    #print("floor before {}".format(yesterday))
    #Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
    for idx in yesterday:
        white(yesterday, toadd, idx-1)
        white(yesterday, toadd, idx+1)
        white(yesterday, toadd, idx-gw)
        white(yesterday, toadd, idx+gw)
        white(yesterday, toadd, idx-(gw+1))
        white(yesterday, toadd, idx+(gw+1))
    for idx in toremove:
        floor.remove(idx)
    for idx in toadd:
        floor.add(idx)
    #print("to remove {}".format(toremove))
    #print("to add {}".format(toadd))
    #print("floor after {}".format(floor))
    print("Day {} : {}".format(day+1, len(floor)))


print()
print(len(floor))


end = time.time()
print("")
print("Done! in {:.3f} ms ".format((end - start)*1000))