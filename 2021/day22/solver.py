
# 2021 Day 22 part 1

import re
from dataclasses import dataclass

f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

# off x=18..30,y=-20..-8,z=-3..13
# on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
regex_mask = r'^(on|off).x=([-0-9]+)\.\.([-0-9]+),y=([-0-9]+)\.\.([-0-9]+),z=([-0-9]+)\.\.([-0-9]+)$'

@dataclass
class Cuboid:
    cmd: str
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int

    def contains_cube(self, px, py, pz):
        return self.x1 <= px <= self.x2 \
               and self.y1 <= py <= self.y2 \
               and self.z1 <= pz <= self.z2


cuboids = []
for line in lines:
    if len(line.strip()) > 0:
        v = re.match(regex_mask, line.strip()).groups()
        c = Cuboid(v[0], int(v[1]), int(v[2]), int(v[3]), int(v[4]), int(v[5]), int(v[6]))
        #print(c)
        cuboids.append(c)

reversed_cuboids = cuboids.copy()
reversed_cuboids.reverse()

total = 0
for x in range(-50, 50+1):
    print("Running x {}".format(x))
    for y in range(-50, 50+1):
        for z in range(-50, 50+1):
            state = False
            for cuboid in reversed_cuboids:
                if cuboid.contains_cube(x, y, z):
                    state = (cuboid.cmd == "on")
                    break
            if state:
                total += 1

print("Part 1 : {}".format(total))

# Part 1 : 543306

