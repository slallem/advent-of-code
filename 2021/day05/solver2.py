
# 2021 Day 5 part 2

import re

#f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

dots = []

rows = []
nb_lines = 0

for line in lines:
    text = line.strip()
    if len(text) == 0:
        # empty line
        nb_lines += 0
    else:
        coords = re.findall(r'([0-9]+)', line)
        coords = list(map(int, coords))
        #print(coords)
        rows.append(coords)


occurences = dict()


def getcharat(i,j):
    zekey = (j*10000)+i
    if zekey not in occurences:
        return '.'
    else:
        return str(occurences[zekey])


def markdot(i,j):
    zekey = (j*10000)+i
    if zekey in occurences:
        occurences[zekey] += 1
    else:
        occurences[zekey] = 1


for r in rows:
    x1 = min(r[0], r[2])
    x2 = max(r[0], r[2])
    y1 = min(r[1], r[3])
    y2 = max(r[1], r[3])
    if x1 == x2:  # vertical
        #print(r)
        for y in range(y1, y2+1):
            markdot(x1, y)
    elif y1 == y2:  # horizontal
        #print(r)
        for x in range(x1, x2+1):
            markdot(x, y1)
    elif abs(x2-x1) == abs(y2-y1):  # diagonal
        #print("diag {}".format(abs(x2-x1)))
        xstep = 1 if r[0] < r[2] else -1
        ystep = 1 if r[1] < r[3] else -1
        xstart = x1 if xstep > 0 else x2
        ystart = y1 if ystep > 0 else y2
        for i in range(0, abs(x2-x1)+1):
            markdot(xstart+(xstep*i), ystart+(ystep*i))


intersect = dict()
# ko py3 -- intersect = dict(filter(lambda (k,v): v > 1, occurences.items()))
for (key, value) in occurences.items():
    if value > 1:
        intersect[key] = value


#print("occurences is {}".format(occurences))
#print("intersect is {}".format(intersect))


for y in range(0, 10):
    txt = ""
    for x in range(0, 10):
        txt += getcharat(x,y)
    print(txt)

print("count is {}".format(len(intersect)))