##!/usr/bin/python3

import time
import re
import itertools


input = [7, 1, 6, 8, 9, 2, 5, 4, 3]
#input = [3,8,9,1,2,5,4,6,7]  # TEST

m = max(input)
for i in range(m, 1000000+1):
    input.append(i)


def rotate_left(liste: list):
    head = liste.pop(0)
    liste.append(head)


def rotate_right(liste: list):
    tail = liste.pop(len(liste)-1)
    liste.insert(0, tail)


def select(liste: list, value: int):
    if value not in liste:
        raise Exception("value should be in list")
    while liste[0] != value:
        rotate_right(liste)
        # print("After rotate {}".format(liste))


# print(min(input))
# print(max(input))
# liste = [1,2,3]
# rotate_right(liste)
# print("{}".format(liste))
# exit(99)

idx = 0
circle = input.copy()
for i in range(1000000):  # 100

    if i % 1000 == 0:
        print("-- Move {} --".format(i+1), flush=True)
        #print("cups: {}".format(circle))

    current_cup = circle[idx]
    # The crab picks up the three cups that are immediately clockwise of the current cup.
    three_cups_picked = [circle[idx+1], circle[idx+2], circle[idx+3]]
    # print("3cups: {}".format(three_cups_picked))
    # They are removed from the circle;
    for cup in three_cups_picked:
        circle.remove(cup)
    # print("newcups: {}".format(circle))
    # cup spacing is adjusted as necessary to maintain the circle.

    # The crab selects a destination cup: the cup with a label equal to the current cup's label minus one.
    value = circle[idx]
    ok = False
    while not ok:
        value -= 1
        if value < min(input):
            value = max(input)
        ok = (value not in three_cups_picked)
        # print("value {} not in {} = {}".format(value, three_cups_picked, ok), flush=True)
    # If this would select one of the cups that was just picked up, the crab will keep subtracting one
    # until it finds a cup that wasn't just picked up.
    # If at any point in this process the value goes below the lowest value
    # on any cup's label, it wraps around to the highest value on any cup's label instead.
    # print("value: {}".format(value))
    select(circle, value)
    # print("cups: {}".format(circle))

    # The crab places the cups it just picked up so that they are immediately clockwise of the destination cup.
    # They keep the same order as when they were picked up.
    for i in range(len(three_cups_picked)):
        circle.insert(i+1, three_cups_picked[i])

    # The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
    select(circle, current_cup)
    rotate_left(circle)


print("Last state {}".format(circle))
