
# 2021 Day 11 part 2

import time

start = time.time()

#f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

carte = dict()
ROWLEN = 20


def setCell(space, x, y, value):
    space[y * ROWLEN + x] = value


def cellExists(space, x, y):
    zekey = y * ROWLEN + x
    return zekey in space.keys()


def getCell(space, x, y):
    if not cellExists(space, x, y):
        return -1
    return space[y * ROWLEN + x]


# Fill space with values
y = 0
for line in lines:
    if len(line) > 0:
        vals = list(line.strip())
        x = 0
        for val in vals:
            setCell(carte, x, y, int(val))
            x += 1
        y += 1

nbcols = x
nbrows = y


def increaseCell(space, x, y, increment):
    cur_val = getCell(space, x, y)
    if cur_val in range(0, 10):
        # value is 0..9
        new_val = cur_val + increment
        setCell(space, x, y, new_val)
        if new_val > 9:  # flashing mode !!! = increase neigbours
            increaseCell(space, x - 1, y - 1, increment)
            increaseCell(space, x - 1, y, increment)
            increaseCell(space, x - 1, y + 1, increment)
            increaseCell(space, x, y - 1, increment)
            increaseCell(space, x, y + 1, increment)
            increaseCell(space, x + 1, y - 1, increment)
            increaseCell(space, x + 1, y, increment)
            increaseCell(space, x + 1, y + 1, increment)


def displaySpace(space, stepnum):
    print()
    print("--- STEP # {}".format(stepnum))
    print()
    for j in range(0, nbrows):
        l = ""
        for i in range (0, nbcols):
            v = getCell(space, i, j)
            c = "."
            if v > 9:
                c = "F"
            else:
                c = str(v)
            l += c
        print(l)


total_flash = 0

#displaySpace(carte, 0)

for step_no in range (1, 1000000+1):
    # Apply step increments
    for j in range(0, nbrows):
        for i in range(0, nbcols):
            increaseCell(carte, i, j, 1)
    # Count flashed cells and resets their value to zero
    step_flash = 0
    for k in carte.keys():
        if carte[k] > 9:
            step_flash += 1
            carte[k] = 0
    total_flash += step_flash
    #displaySpace(carte, step_no)
    #print("Step {} : adding {} flashes, total {}".format(step_no, step_flash, total_flash))
    if sum(carte.values()) == 0:
        print("Step {} : only zeroes".format(step_no))
        break


