
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


# F10
# N3
# F7
# R90
# F11


def decode_ligne(data):
    res = dict()
    res["code"] = data[0]
    res["val"]= int(data[1:])
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
    #print("number of lines {}".format(nb_lines))
    return res


start = time.time()

# regex_examples()
# print(combinations(["A", "B", "C"], range(2,3)))
# print(combinations(["X", "Y", "Z"]))

commands = read_file('input.txt')


man_e = 0
man_n = 0
# directions = east=0, south=1, west=2, north =3
direction = 0



for cmd in commands:
    code = cmd["code"]
    val = cmd["val"]
    print("{} {}".format(code, val))
    # Action N means to move north by the given value.
    if code == "N":
        man_n += val
    # Action S means to move south by the given value.
    elif code == "S":
        man_n -= val
    # Action E means to move east by the given value.
    elif code == "E":
        man_e += val
    # Action W means to move west by the given value.
    elif code == "W":
        man_e -= val
    # Action L means to turn left the given number of degrees.
    elif code == "L":
        direction = (direction - (val/90)) % 4
    # Action R means to turn right the given number of degrees.
    elif code == "R":
        direction = (direction + (val/90)) % 4
    # Action F means to move forward by the given value in the direction the ship is currently facing.
    elif code == "F":
        if direction == 0:  # East
            man_e += val
        elif direction == 1:  # South
            man_n -= val
        elif direction == 2:  # West
            man_e -= val
        elif direction == 3:  # North
            man_n += val
    print("  N {} E {} dir {}".format(man_n, man_e, direction))

print("N {} E {} --> {}".format(-man_n, man_e, -man_n + man_e))

print("N {} E {} --> {}".format(-man_n, man_e, man_n + -man_e))


end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))