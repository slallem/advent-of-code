
# 2021 Day 22 part 2

# I should have use another language for this one...
# Python spaghetti yum yum!

# Idee
# Parcourir la liste des Cuboides à l'envers ce qui évite beacoup de process inutile
# il est en effet idiot de calculer des cuboides (entiers ou fragmentés) pour les supprimer derrière
# autant ne pas les prendre en compte si on sait (en prenant les offs à rebrousse poil)
# quand on tombe sur du ON, on ajoute à la liste en faisant attention aux doublons (i.e fragmenter) => fct union
# quand on tombe sur du OFF, on ajoute à la liste des zones "interdites"


import re
from dataclasses import dataclass

f = open('input_ex2.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

# off x=18..30,y=-20..-8,z=-3..13
# on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
regex_mask = r'^(on|off).x=([-0-9]+)\.\.([-0-9]+),y=([-0-9]+)\.\.([-0-9]+),z=([-0-9]+)\.\.([-0-9]+)$'


def calc_segments(start, stop, via1, via2):
    if start <= via1 <= stop and start <= via2 <= stop:
        # Divide in 3 segments
        return [[start, via1-1], [via1, via2], [via2+1, stop]]
    elif start <= via1 <= stop:
        # Divide in 2 segments (right include via)
        return  [[start, via1-1], [via1, stop]]
    elif start <= via2 <= stop:
        # Divide in 2 segments (left include via)
        return  [[start, via2], [via2+1, stop]]
    #  Single segment
    return [[start, stop]]


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

    def count_contained(self, cubes):
        res = 0
        for cube in cubes:
            if self.contains_cube(cube[0], cube[1], cube[2]):
                res += 1
        return res

    def contains_all(self, cubes):
        return int(self.count_contained(cubes)) == len(cubes)

    def size(self):
        # Size = Number of contained cubes = (Width x Height x Depth)
        return max(0, (self.x2 - self.x1 + 1)) * max(0, (self.y2 - self.y1 + 1)) * max(0, (self.z2 - self.z1 + 1))

    def is_valid(self):
        return self.x1 <= self.x2 and self.y1 <= self.y2 and self.z1 <= self.z2

    def corners(self):
        corners = [(self.x1, self.y1, self.z1),
                   (self.x1, self.y1, self.z2),
                   (self.x1, self.y2, self.z1),
                   (self.x1, self.y2, self.z2),
                   (self.x2, self.y1, self.z1),
                   (self.x2, self.y1, self.z2),
                   (self.x2, self.y2, self.z1),
                   (self.x2, self.y2, self.z2)]
        return corners

    def intersects(self, c2):
        crossx = not ((c2.x1 < self.x1 and c2.x2 < self.x1) or (c2.x1 > self.x2 and c2.x2 > self.x2))
        crossy = not ((c2.y1 < self.y1 and c2.y2 < self.y1) or (c2.y1 > self.y2 and c2.y2 > self.y2))
        crossz = not ((c2.z1 < self.z1 and c2.z2 < self.z1) or (c2.z1 > self.z2 and c2.z2 > self.z2))
        return crossx and crossy and crossz

    def split_erase(self, c2):
        # Remove a cuboid zone from this cuboid (if C2 is contained or intersects this one)
        # i.e. Explodes the cuboid into several cuboids (between 0 and 26 sub cubes)
        #if not self.intersects(c2):
        #    # Cuboids are not related, cube remains the same
        #    print("Cuboids are not related")
        #    return [self]
        if c2.contains_all(self.corners()):
            # Cuboid c2 contains all this cuboid = erases it entirely
            #print("Cuboid c2 contains all this cuboid")
            return []
        # Cubes are overlapping
        # Split this Cuboid into 27 possible sub-cuboids
        res = []
        i = 0
        x_segments = calc_segments(self.x1, self.x2, c2.x1, c2.x2)
        y_segments = calc_segments(self.y1, self.y2, c2.y1, c2.y2)
        z_segments = calc_segments(self.z1, self.z2, c2.z1, c2.z2)
        #print("x seg {}".format(x_segments))
        #print("y seg {}".format(y_segments))
        #print("z seg {}".format(z_segments))
        for xs in x_segments:
            for ys in y_segments:
                for zs in z_segments:
                    i += 1
                    sc = Cuboid("on", xs[0], xs[1], ys[0], ys[1], zs[0], zs[1])
                    #print("Evaluation #{} SubCuboid {} size {} valid {} contained in c2 {}".format(i, sc, sc.size(), sc.is_valid(), c2.contains_all(sc.corners())))
                    if sc.is_valid() and sc.size() > 0:  # ignore invalid cubes
                        if not c2.contains_all(sc.corners()):  # do not include split cuboids inside erased zone
                            res.append(sc)
        return res


def exists_in_list(item, liste):
    for c in liste:
        if c.contains_all(item.corners()):
            return True
    return False


def simplify(liste):
    newliste = []
    liste.sort(key=lambda x: -x.size())
    while len(liste) > 0:
        item = liste.pop()
        if not exists_in_list(item, liste):
            newliste.append(item)
    return newliste

cuboids = []
for line in lines:
    if len(line.strip()) > 0:
        v = re.match(regex_mask, line.strip()).groups()
        c = Cuboid(v[0], int(v[1]), int(v[2]), int(v[3]), int(v[4]), int(v[5]), int(v[6]))
        #print(c)
        cuboids.append(c)


reversed_cuboids = cuboids.copy()
reversed_cuboids.reverse()


def fragmenter(cub, lon, loff):
    remains = [cub]
    for off in loff:
        newremains = []
        for r in remains:
            if r.intersects(off):
                splitted = r.split_erase(off)
                for sp in splitted:
                    newremains.append(sp)
            else:
                newremains.append(r)  # no split
        remains = newremains
    for on in lon:
        newremains = []
        for r in remains:
            if r.intersects(on):
                splitted = r.split_erase(on)  # erased part already exists in "ons"
                for sp in splitted:
                    newremains.append(sp)
            else:
                newremains.append(r)
        remains = newremains
    return remains


ons = []
offs = []
i = 0
nb = len(reversed_cuboids)
for c in reversed_cuboids:
    i += 1
    print("Processing step {} of {} (ons size {} offs size {})".format(i, nb, len(ons), len(offs)))
    #print("Processing {}".format(c))
    if c.cmd == "on":
        # fragmenter en tenant compte des zones exclues (offs) et des zones sûres déjà connues (ons)
        subs = fragmenter(c, ons, offs)
        for sub in subs:
            ons.append(sub)
        #ons.sort(key=lambda x: -x.size())
    elif c.cmd == "off":
        offs.append(c)
        #offs.sort(key=lambda x: -x.size())

active_cuboids = ons


#Some UTs
# print("---------")
# c1 = Cuboid("on",  1, 3,  1, 3,  1, 3)
# print(c1, c1.size())
# c2 = Cuboid("off",  -2, 2,  2, 2,  3, 3)
# print(c2, c2.size())
# print("intersects {}".format(c1.intersects(c2)))
# print("intersects {}".format(c2.intersects(c1)))
# subcuboids = c1.split_erase(c2)
# for cuboid in subcuboids:
#     print(cuboid, cuboid.size())
# print(len(subcuboids))
# print(sum(v.size() for v in subcuboids))
#print(calc_segments(1, 3, -2, 2))

# Tentative de calcul en marche avant...
# active_cuboids = list()
# i = 0
# nb = len(cuboids)
# for cuboid in cuboids:
#     # Split others and remove this cuboid space
#     i += 1
#     print("Processing step {} of {} (cuboids list size {}".format(i, nb, len(active_cuboids)))
#     #print("before {}".format(active_cuboids))
#     if cuboid.cmd == "off":
#         new_active = list()
#         for c in active_cuboids:
#             subs = c.split_erase(cuboid)
#             for sub in subs:
#                 new_active.append(sub)
#         active_cuboids = new_active  # replace
#     # If this new cuboid is on, add it "as is" as its space must be counted
#     elif cuboid.cmd == "on":
#         active_cuboids.append(cuboid)
#         active_cuboids = simplify(active_cuboids)

    #print("after {}".format(active_cuboids))


# Compute total
total = 0
for cuboid in active_cuboids:
    total += cuboid.size()

#print("Part 2 should be 2758514936282235") # fro given example
print("Part 2 is....... {}".format(total))

# 1285501151402480


