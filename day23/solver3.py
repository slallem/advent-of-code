##!/usr/bin/python3

import time
import re
import itertools
import cProfile

# tentative d'optimisation par liste double chainée
# bien mieux comme cela !!!! (~25 secondes pour 10M itérations)


class Cup:
    value: int = 0
    next: 'Cup' = None


def display_circle(start_cup, highlight_cup=None):
    res = ""
    cup = start_cup
    while True:
        if cup is None:
            break  # sequence terminated (not a loop)
        if cup == start_cup and len(res) > 0:
            break  # loop complete
        if cup == highlight_cup:
            res += " ({})".format(cup.value)
        else:
            res += " {}".format(cup.value)
        cup = cup.next
    return res


def solve_puzzle_od_day_23_part2():

    # ------------------------------------------------------
    # Raw input
    # ------------------------------------------------------

    input = [7, 1, 6, 8, 9, 2, 5, 4, 3]  # My input
    # input = [3, 8, 9, 1, 2, 5, 4, 6, 7]  # TEST
    verbose = False
    iterations = 10000000

    m = max(input)
    for i in range(m, 1000000):
        input.append(i+1)

    # ------------------------------------------------------
    # Double-linked list + value-indexed dictionary
    # ------------------------------------------------------

    cups_by_value = dict()
    nbcups = len(input)
    all_cups = list()
    for i in range(nbcups):
        all_cups.append(Cup())
    for i in range(nbcups):
        all_cups[i].value = input[i]
        all_cups[i].next = all_cups[(i+1) % nbcups]
        cups_by_value[all_cups[i].value] = all_cups[i]

    # ------------------------------------------------------
    # Iterations...
    # ------------------------------------------------------

    current_cup = all_cups[0]
    for i in range(iterations):
        if verbose:
            print()
        if ((i+1) % 100000 == 0) or (nbcups < 100) or (i == 0) or (i == 9):
            print("-- Move {} --".format(i+1), flush=True)
        if verbose:
            print("cups: {}".format(display_circle(current_cup, current_cup)))
        if verbose:
            print("current cup: {}".format(current_cup.value))
        # The crab picks up the three cups that are immediately clockwise of the current cup.
        # three_cups_picked = [circle[(idx+1) % nbcups], circle[(idx+2) % nbcups], circle[(idx+3) % nbcups]]
        # They are removed from the circle;
        cup1 = current_cup.next
        cup2 = cup1.next
        cup3 = cup2.next
        current_cup.next = cup3.next  # remove the 3 cups (shunt current cup to the 4th cup)
        cup3.next = None

        if verbose:
            print("3cups: {} {} {}".format(cup1.value, cup2.value, cup3.value))

        # The crab selects a destination cup: the cup with a label equal to the current cup's label minus one.
        dest_cup_value = current_cup.value
        ok = False
        while not ok:
            dest_cup_value -= 1
            if dest_cup_value < 1:  # == min(input):
                dest_cup_value = len(input)  # == max(input)
            ok = (dest_cup_value != cup1.value and dest_cup_value != cup2.value and dest_cup_value != cup3.value)
        # If this would select one of the cups that was just picked up, the crab will keep subtracting one
        # until it finds a cup that wasn't just picked up.
        # If at any point in this process the value goes below the lowest value
        # on any cup's label, it wraps around to the highest value on any cup's label instead.
        if verbose:
            print("destination: {}".format(dest_cup_value))

        # The crab places the cups it just picked up so that they are immediately clockwise of the destination cup.
        # They keep the same order as when they were picked up.
        # for i in range(3):
        #     dest_idx = (dest_idx+1) % len(circle)
        #     cup_to_insert = three_cups_picked[i]
        #     circle.insert(dest_idx, cup_to_insert)
        #     if dest_idx <= idx:
        #         idx += 1  # shifts current index if some inserted before it
        insert_after = cups_by_value[dest_cup_value]
        insert_before = insert_after.next
        insert_after.next = cup1
        cup3.next = insert_before

        # The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
        current_cup = current_cup.next
        if verbose:
            print("newcups: {}".format(display_circle(current_cup, current_cup)))

    solution = ""
    cup1 = cups_by_value[1]
    cup = cup1
    for i in range(9):
        cup = cup.next
        solution += "{} ".format(cup.value)

    print()
    print("Soluce for part 1 is {}".format(solution))

    # if (solution.replace(" ","") == "926583741"):
    #     print("OK!")
    # else:
    #     print("**KO**")

    print()
    print("Soluce for part 2 is {} * {} = {}".format(cup1.next.value, cup1.next.next.value, cup1.next.value * cup1.next.next.value))

# Profiling tips
# cProfile.run(solve_puzzle_od_day_23_part2())
# python -m cProfile solver3.py

start = time.time()

solve_puzzle_od_day_23_part2()

end = time.time()
print("")
print("Done! in {:.3f} ms ".format((end - start)*1000))