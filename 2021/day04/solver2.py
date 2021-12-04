
# 2021 Day 4 part 2

#f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

draws = lines[0].split(",")
del lines[0]  # remove header

rows = []
nb_lines = 0

for line in lines:
    text = line.strip()
    if len(text) == 0:
        # empty line
        nb_lines += 0
    else:
        rows.append(line.split())

drawn = []
last = -1

nbplayers = len(rows)//5
grids = []

for p in range(0, nbplayers):
    grids.append([])
    for r in range(0, 5):
        crow = []
        for c in range(0, 5):
            crow.append(rows[(p*5)+r][c])
        grids[p].append(crow)

for p in range(0, nbplayers):
    for c in range(0, 5):
        ccol = []
        for r in range(0, 5):
            ccol.append(rows[(p*5)+r][c])
        grids[p].append(ccol)

winnners = []
losers = list(range(0, nbplayers))

for draw in draws:
    last = int(draw)
    drawn.append(last)
    for p in range(0, nbplayers):
        if p in losers:
            for grid in grids[p]:
                if draw in grid:
                    grid.remove(draw)
                    if len(grid) == 0:
                        # winner condition
                        if p not in winnners:
                            winnners.append(p)
                        if len(losers) > 1:
                            if p in losers:
                                losers.remove(p)
    if len(winnners) == nbplayers:  # = the last one wins
        break

print("winners {} losers {}".format(winnners, losers))

# Calc result

loser = losers[0]

sum = 0
for g in range(0, 5):
    for n in grids[loser][g]:
        print(n)
        sum += int(n)

print("last is {}".format(last))
print("sum of remaining is {}".format(sum))

print("solution is {}".format(last * sum))