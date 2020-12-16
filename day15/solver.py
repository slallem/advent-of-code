#!/usr/bin/python
# -*- coding: <encoding name> -*-

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


def decode_ligne(data):
    res = data #list(data)
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

#lines = read_file('input.txt')


# def last_index_of(liste: list, val: int):
#     res = -1
#     for i in range(len(liste)):
#         if liste[i] == val:
#             res = i
#     return res

def last_index_of(liste: list, val: int):
    res = -1
    for i in range(len(liste)-1, 0, -1):
        if liste[i] == val:
            res = i
            break
    return res

input = "1,0,15,2,10,13"
#input = "3,1,2"
#input = "0,3,6"

snums = input.split(",")

last_indexes = dict()

turn = 0
for ii in range(len(snums)-1):
    snum = snums[ii]
    turn += 1
    last_indexes[int(snum)] = turn
    print("turn {} last said {}".format(turn, snum))

last_said = int(snums[-1])
while True:
    turn += 1

    lasti: int = -1
    if last_said in last_indexes.keys():
        lasti = last_indexes[last_said] - 1
    last_indexes[last_said] = turn

    #print("   lastindex of {} is {}".format(last_said, lasti))
    if lasti < 0:
        say = 0
    else:
        #print("   last index of {} is {}".format(last_said, lasti))
        say = turn - lasti - 1
    last_said = say
    if turn % 200000 == 0:
        print("turn {} says {}".format(turn+1, last_said))

    if turn == (30000000 - 1):
    #if turn == (2020 - 1):
    #if turn >= 10:
        print("turn {} says {}".format(turn+1, last_said))
        break


#print("number of lines {}".format(len(lines)))


end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))