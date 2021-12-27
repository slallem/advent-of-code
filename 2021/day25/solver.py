
# 2021 Day 25 part 1

import copy

#f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

sea_floor = []
for line in lines:
    if len(line.strip()) > 0:
        sea_floor.append(list(line.strip()))


def do_moves(insea):
    sea = copy.deepcopy(insea)
    height = len(sea)
    width = len(sea[0])
    #print(f"h {height} w {width}")
    swaps = []
    # East facing first
    for y in range(0, height):
        for x in range(0, width):
            if sea[y][x] == '>':
                #print(f"found > at row {y} col {x}")
                if sea[y][(x+1) % width] == '.':
                    swaps.append([[y, x], [y, (x+1) % width]])
    for swap in swaps:
        tmp = sea[swap[0][0]][swap[0][1]]
        sea[swap[0][0]][swap[0][1]] = sea[swap[1][0]][swap[1][1]]
        sea[swap[1][0]][swap[1][1]] = tmp
    swaps = []
    # Then south facing
    for x in range(0, width):
        for y in range(0, height):
            if sea[y][x] == 'v':
                #print(f"found v at row {y} col {x}")
                if sea[(y+1) % height][x] == '.':
                    swaps.append([[y, x], [(y+1) % height, x]])
    for swap in swaps:
        tmp = sea[swap[0][0]][swap[0][1]]
        sea[swap[0][0]][swap[0][1]] = sea[swap[1][0]][swap[1][1]]
        sea[swap[1][0]][swap[1][1]] = tmp
    return sea


step = 0
while True:
    step += 1
    new_sea_floor = do_moves(sea_floor)
    #print(sea_floor)
    #print(new_sea_floor)
    if new_sea_floor == sea_floor:
        # no changes
        print(f"no change at step {step}")
        break
    sea_floor = new_sea_floor
