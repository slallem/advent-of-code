
# 2021 Day 10 part 2

# Tip: Do not forget to read the specs !
# Here ware about valid but INCOMPLETE lines (not corrupted ones !!! :)

import time

start = time.time()

f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

ref = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

refco = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<"
}

score_table = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

score_tbclo = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

def isOpening(c):
    return c in ref.keys()


def isClosing(c):
    return c in refco.keys()


def isClosingThat(c, o):
    return c == ref[o]

errors = []

def isValidChunck(s):
    global errors
    stack = []
    for c in list(s):
        if isOpening(c):
            # OK, add stack then next
            #print("ok {} is opening".format(c))
            stack.append(c)
        elif isClosing(c):
            #print("ok {} is closing".format(c))
            #Is closing the right last opened bracket?
            lastopen = stack.pop()
            if not isClosingThat(c, lastopen):
                errors.append("Unexpected char")
                return -1  # don't care !!!
        else:
            #not a bracket
            print("ERROR {} is not a bracket".format(c))
            exit(9)
    if len(stack) > 0:
        # incomplete
        rest = []
        while len(stack) > 0:
            rest.append(ref[stack.pop()])
        print(" rest is {}".format("".join(rest)))
        sc = 0
        for cc in rest:
            sc *= 5
            sc += score_tbclo[cc]
        return sc
    return -1


scores = []
for line in lines:
    if len(line) > 0:
        sc = isValidChunck(line.strip())
        if sc >= 0:
            scores.append(sc)


scores.sort()
print(scores)

print(scores[len(scores)//2])

end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))
