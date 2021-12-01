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
    items = re.findall(r"[+0-9]+|[*]", expr)
    xp2 = ""
    for item in items:
        if "+" in item:
            xp2 += str(eval(item))
        else:
            xp2 += item
    res = eval(xp2)
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

print("Part #2 total {}".format(total))

end = time.time()
print("")
print("Done! in {:.3f} ms ".format((end - start)*1000))
