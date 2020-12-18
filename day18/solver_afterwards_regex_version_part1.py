#!/usr/bin/python3

import time
import re


def read_file(filename):
    res = list()
    f = open(filename, 'r')
    for text_line in f.readlines():
        text = text_line.strip()
        if len(text) > 0:
            res.append(text)
    return res


def eval_expr(expr: str):
    res = expr
    while True:
        match = re.match(r"^([0-9]+[+*][0-9]+)([+*].+)$", res)
        if match is None:
            break
        groupes = match.groups()
        res = str(eval(groupes[0])) + groupes[1]
    res = eval(res)
    return res


def eval_ligne(expression):
    res = expression.replace(" ", "")
    while True:
        match = re.match(r'^(.*)[(]([*+0-9]+)[)](.*)$', res)
        if match is None:
            break
        groupes = match.groups()
        res = groupes[0] + str(eval_expr(groupes[1])) + groupes[2]
    res = eval_expr(res)
    return res


# --------------------------------------------
#                    M A I N
# --------------------------------------------

lines = read_file('input.txt')

# Quelques TU
# print(eval_ligne("1 + (2 * 3) + (4 * (5 + 6))"))
# print(eval_ligne("2 * 3 + (4 * 5)"))
# print(eval_ligne("5 + (8 * 3 + 9 + 3 * 4 * 3)"))
# print(eval_ligne("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"))
# print(eval_ligne("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"))

start = time.time()

total = 0
for line in lines:
    total += eval_ligne(line)

print("Part #1 total {}".format(total))

end = time.time()
print("")
print("Done! in {:.3f} ms ".format((end - start)*1000))
