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

# lines = read_file('input.txt')
# print("number of lines {}".format(len(lines)))

player1 = [10,39,16,32,5,46,47,45,48,26,36,27,24,37,49,25,30,13,23,1,9,3,31,14,4]
player2 = [2,15,29,41,11,21,8,44,38,19,12,20,40,17,22,35,34,42,50,6,33,7,18,28,43]

turn = 0
while True:
    turn += 1
    p1 = player1.pop(0)
    p2 = player2.pop(0)
    ma = max(p1,p2)
    mi = min(p1,p2)
    if p1 > p2:
        # p1 wins
        player1.append(ma)
        player1.append(mi)
    else:
        # p2 wins
        player2.append(ma)
        player2.append(mi)
    if len(player1) == 0 or len(player2) == 0:
        break

print("P1 {}".format(player1))
print("P2 {}".format(player2))

# calculate score
score = 0
deck = player1
if len(player1) == 0:
    deck = player2

tot = 0
for i in range(1, len(deck)+1):
    print("{} * {} = {}".format(deck[len(deck)-i], i, deck[len(deck)-i]*i))
    tot += (deck[len(deck)-i] * i)
print("TOTAL SCORE {}".format(tot))


end = time.time()
print("")
print("Done! in {:.3f} ms ".format((end - start)*1000))