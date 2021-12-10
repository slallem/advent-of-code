
# 2021 Day 9 part 2

import time

start = time.time()

#f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

carte = dict()
storage_width = 100
disp = []

# Fill space with values
y = 0
for line in lines:
    if len(line) > 0:
        disp.append(list(line.strip()))
        vals = list(line.strip())
        x = 0
        for val in vals:
            carte[y * 100 + x] = int(val)
            x += 1
        y += 1

# Part 1 find lowest spots

nbcols = x
nbrows = y

sum = 0
lowspots = []
for y in range(0, nbrows):
    for x in range(0, nbcols):
        value = carte[y * storage_width + x]
        comparisons = []
        if y > 0:
            comparisons.append(carte[(y - 1) * storage_width + x])
        if (y < nbrows-1):
            comparisons.append(carte[(y + 1) * storage_width + x])
        if x > 0:
            comparisons.append(carte[y * storage_width + x - 1])
        if x < nbcols-1:
            comparisons.append(carte[y * storage_width + x + 1])
        nblower = 0
        for comp in comparisons:
            if value < comp:
                nblower += 1
        if nblower == len(comparisons):
            # print("Found {} at pos x:{} y:{}".format(value, x, y))
            sum += value + 1
            lowspots.append(y * storage_width + x)

print("Part one: Found {} lowspots with a risk level sum of {}".format(len(lowspots), sum))


print()
print("Part two")

# From carte (whole map values as reference),
# Keep track of all 9's (aka "walls")
# Keep track of other remaining spots in basin search

walls = []
spots = []
for k in carte.keys():
    if carte[k] >= 9:
        walls.append(k)
    else:
        spots.append(k)


# --Then take one spot and recursively find its all adjacent pals <-- NOPE !
# Just start from lowest points identified in part #1 (D'oh!)

# Recursive way
def getBasin(key, curval, spots):
    value = 0
    if key in spots:  # avoids walls or already seen spots
        spotval = carte[key]
        #if spotval > curval:  # only count it when ground goes up
        value += 1  # The size of a basin is the number of locations within the basin
        spots.remove(key)  # prevents infinite loops (important!)
        cx = key % storage_width
        cy = key // storage_width
        disp[cy][cx] = '-'
        #if cx > 0:
        value += getBasin(key-1, spotval, spots)
        #if cx < nbcols-1:
        value += getBasin(key+1, spotval, spots)
        #if cy > 0:
        value += getBasin(key-storage_width, spotval, spots)
        #if cy < nbrows-1:
        value += getBasin(key+storage_width, spotval, spots)
    return value


basins = []

iter = 0
while len(spots) > 0:
#for ls in lowspots:
    ls = spots[0]
    basin = getBasin(ls, -1, spots)
    disp[ls // storage_width][ls % storage_width] = '.'
    basins.append(basin)
    #print("Found basin {}".format(basin))
    iter +=1
    #if iter>2:
    #    break

basins.sort(reverse=True)

print("Found {} basins (sorted largest to smallest): {}".format(len(basins), basins))
print()

#print("What do you get if you multiply together the sizes of the three largest basins?")
#print(basins[0] * basins[1] * basins[2])


end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))

# DISPLAY OUTPUT GRAPHICALLY (ASCII)
print()
for y in disp:
    txt = ""
    for x in y:
        txt += x
    print(txt)