
# 2021 Day 19 part 1 and 2

# ~10mn computation time
# NOTA: this implementation works but is not the most efficient
# because it checks each scanner data with the global live-built puzzle too many times
# It should be better if checked 2 by 2
# I guess many optimizations are still possible to avoid pointless comparisons

import itertools
import time

start = time.time()

#f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

# Rotations
# 0, 1=90, 2=180, 3=270
# Rotations are assumed from 0,0,0 point

def rotate_xy(pt):
    return -pt[1], pt[0], pt[2]


def rotate_yz(pt):
    return pt[0], -pt[2], pt[1]


def rotate_xz(pt):
    return pt[2], pt[1], -pt[0]


def translate_point(p: list, offset: list):
    return p[0]+offset[0], p[1]+offset[1], p[2]+offset[2]


def translate_points(pts: list, offset: list):
    res = []
    for pt in pts:
        res.append(translate_point(pt, offset))
    return res


def negate(p):
    return [-p[0], -p[1], -p[2]]


def rotate_points(points, rot_xy, rot_yz, rot_xz):
    res = []
    for point in points:
        newp = point
        for nx in range(0, rot_xy):
            newp = rotate_xy(newp)
        for ny in range(0, rot_yz):
            newp = rotate_yz(newp)
        for nz in range(0, rot_xz):
            newp = rotate_xz(newp)
        res.append(newp)
    return res


# ------------- Read input file
scans = dict()
idx = -1
for raw_line in lines:
    line = raw_line.strip()
    if len(line) > 0:
        if "scanner" in line:
            # Scanner header
            idx += 1
            scans[idx] = []
        else:
            # Beacon coordinates
            values = line.split(",")
            scans[idx].append((int(values[0]), int(values[1]), int(values[2])))

scanner_coords = dict()

# Consider scan 0 as reference for orientation
area = set()
for p in scans[0]:  # all beacons from scanner 0 are good
    area.add(p)
del scans[0]

while len(scans.keys()) > 0:
    for k in scans.keys():
        # Scanner is candidate for a test-match
        # For every rotation
        print(f"Searching matchings for Scanner#{k}")
        matchfound = False
        rots = 4  # half rotation on all plans are sufficient
        for rxz in range(0, rots):
            for ryz in range(0, rots):
                for rxy in range(0, rots):
                    # Apply rotations 0,90,180,270 on 3 axis
                    rotated = rotate_points(scans[k], rxy, ryz, rxz)
                    for rpt in rotated:
                        # translate rotated points relatively to one of its points
                        translated_relative = translate_points(rotated, negate(rpt))
                        #print(translated_relative) # OK
                        # Check every known absolute points as if they were offsets
                        for p_ref in area:
                            # p_ref is in absolute coordinates (as are all points in area)
                            # Translate all points in absolute coordinates (relative from p_ref = absolute)
                            translated_absolute = translate_points(translated_relative, p_ref)
                            # Then count points matching known points
                            tested = 0
                            matching = 0
                            for pa in translated_absolute:
                                tested += 1
                                if pa in area:
                                    matching += 1
                                    if matching >= 12:  # early stop
                                        break
                            #print(f"rotated {rx},{ry},{rz} testing offset {p_ref} = match: {matching}")
                            if matching >= 12:
                                print(f"rotated {rxy},{ryz},{rxz} testing offset {p_ref} = match: {matching}")
                                # match found
                                print("Match found for Scanner #{}".format(k))
                                matchfound = True
                                # add all points (in absolute coordinates) for those not already known
                                for pt in translated_absolute:
                                    area.add(pt)  # does nothing iof already exists in set
                                del scans[k]  # remove this scanner once it completes the puzzle ...
                                # translate scanner coordinate to absolute coordinates within global area
                                scanner_center_relative = translate_point((0, 0, 0), negate(rpt))
                                scanner_center_absolute = translate_point(scanner_center_relative, p_ref)
                                scanner_coords[k] = scanner_center_absolute
                                break
                        if matchfound:
                            break
                    if matchfound:
                        break
                if matchfound:
                    break
            if matchfound:
                break
        if matchfound:
            break
        #next candidate (more than one scanner can be overlap this one)

# ---- Part 1

print()
print(f"Part #1 Beacon count is {len(area)}")

# ---- Part 2

print()
#print(scanner_coords)

mds = dict()
perms = list(itertools.permutations(scanner_coords.keys(), 2))
#print(perms)
for perm in perms:
    # calculate Manhattan distance between two points
    pt1 = scanner_coords[perm[0]]
    pt2 = scanner_coords[perm[1]]
    md = abs(pt1[0]-pt2[0]) + abs(pt1[1]-pt2[1]) + abs(pt1[2]-pt2[2])
    mds[perm] = md
#print(mds)
print(f"Part #2 Largest distance between 2 scanners is {max(mds.values())}")

end = time.time()
print("")
print("Done! in {:.3f} s ".format(end - start))




