
# 2021 Day 5 part 1

import re
f = open('input_ex.txt', 'r')
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


def markdot(i,j):
    #global occurences
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

intersect = dict()
# ko py3 -- intersect = dict(filter(lambda (k,v): v > 1, occurences.items()))
for (key, value) in occurences.items():
    if value > 1:
        intersect[key] = value


#print("occurences is {}".format(occurences))
#print("intersect is {}".format(intersect))

print("count is {}".format(len(intersect)))