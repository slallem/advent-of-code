
# 2021 Day 10 part 1

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
                return score_table[c]
        else:
            #not a bracket
            print("ERROR {} is not a bracket".format(c))
            exit(9)
    #if len(stack) > 0:
    #    print("ERROR Stack {} should be empty".format(stack))
    #    exit(9)
    return 0


scores = []
for line in lines:
    if len(line) > 0:
        scores.append(isValidChunck(line.strip()))


print(scores)

print(sum(scores))

end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))
