##!/usr/bin/python3

import time
import re
import itertools
import cProfile


def resolve_puzzle_od_day_23_part2():
    input = [7, 1, 6, 8, 9, 2, 5, 4, 3]
    verbose = False
    iterations = 1000000

    m = max(input)
    for i in range(m, 1000000):
        input.append(i+1)

    # input = [3,8,9,1,2,5,4,6,7]  # TEST
    # iterations = 10
    # verbose = True


    nbcups = len(input)

    idx = 0
    circle = input.copy()
    for i in range(iterations):
        if verbose:
            print()
        if (i % 1000 == 0) or (nbcups < 100):
            print("-- Move {} --".format(i+1), flush=True)
        if verbose:
            print("cups: {}".format(circle))
        current_cup = circle[idx % nbcups]
        if verbose:
            print("current cup: {}".format(current_cup))
        # The crab picks up the three cups that are immediately clockwise of the current cup.
        # three_cups_picked = [circle[(idx+1) % nbcups], circle[(idx+2) % nbcups], circle[(idx+3) % nbcups]]
        # They are removed from the circle;
        # for cup in three_cups_picked:
        #     circle.remove(cup)
        index1 = (idx+1) % len(circle)
        cup1 = circle.pop(index1)
        index2 = index1 % len(circle)
        cup2 = circle.pop(index2)
        index3 = index2 % len(circle)
        cup3 = circle.pop(index3)
        # shiftes current index if some removed before it
        if index1 < idx:
            idx -= 1
        if index2 < idx:
            idx -= 1
        if index3 < idx:
            idx -= 1

        if verbose:
            print("3cups: {} {} {}".format(cup1, cup2, cup3))

        # if verbose:
        #     print("newcups: {}".format(circle))
        # cup spacing is adjusted as necessary to maintain the circle.

        # The crab selects a destination cup: the cup with a label equal to the current cup's label minus one.
        dest_cup = current_cup
        ok = False
        while not ok:
            dest_cup -= 1
            if dest_cup < 1:  # min(input):
                dest_cup = len(input)  # max(input)
            ok = (dest_cup != cup1 and dest_cup != cup2 and dest_cup != cup3)
            # if verbose:
            #     print("value {} not in {} = {}".format(dest_cup, three_cups_picked, ok), flush=True)
        # If this would select one of the cups that was just picked up, the crab will keep subtracting one
        # until it finds a cup that wasn't just picked up.
        # If at any point in this process the value goes below the lowest value
        # on any cup's label, it wraps around to the highest value on any cup's label instead.
        if verbose:
            print("destination: {}".format(dest_cup))
        dest_idx = circle.index(dest_cup) % len(circle)
        if verbose:
            print("destination index is {} in list {}".format(dest_idx, circle))

        # The crab places the cups it just picked up so that they are immediately clockwise of the destination cup.
        # They keep the same order as when they were picked up.
        # for i in range(3):
        #     dest_idx = (dest_idx+1) % len(circle)
        #     cup_to_insert = three_cups_picked[i]
        #     circle.insert(dest_idx, cup_to_insert)
        #     if dest_idx <= idx:
        #         idx += 1  # shifts current index if some inserted before it
        dest_idx = (dest_idx+1) % len(circle)
        circle.insert(dest_idx, cup1)
        if dest_idx <= idx:
            idx += 1  # shifts current index if some inserted before it
        dest_idx = (dest_idx+1) % len(circle)
        circle.insert(dest_idx, cup2)
        if dest_idx <= idx:
            idx += 1  # shifts current index if some inserted before it
        dest_idx = (dest_idx+1) % len(circle)
        circle.insert(dest_idx, cup3)
        if dest_idx <= idx:
            idx += 1  # shifts current index if some inserted before it

        if verbose:
            print("newcups: {}".format(circle))
        # The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
        # --idx = circle.index(current_cup) % nbcups
        idx = (idx + 1) % nbcups
        # idx = select(circle, current_cup) % len(circle)
        if verbose:
            print("new current cup will be: {} at index {}".format(circle[idx % nbcups], idx))


    print("Last state {}".format(circle))
    print()

    soluce = ""
    idx1 = circle.index(1)
    for i in range(9):
        soluce += "{} ".format(circle[(idx1+i+1) % len(circle)])

    print("Soluce {}".format(soluce))

    if (soluce.replace(" ","") == "926583741"):
        print("OK!")
    else:
        print("**KO**")



#cProfile.run(resolve_puzzle_od_day_23_part2())

resolve_puzzle_od_day_23_part2()
