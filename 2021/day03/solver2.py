
# 2021 Day 3 part 2

#f = open('input-debug.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

varlen = len(lines[0])-1
print(varlen)

remaining = []
for row in lines:
    value = int(row, 2)
    remaining.append(value)


print("remains {}".format(len(remaining)))
for i in range(0, varlen):
    mask = 1 << (varlen-1-i)
    print("mask {} remaining {}".format(mask, remaining))
    zeroes = 0
    ones = 0
    for value in remaining:
        if value & mask == mask:
            ones += 1
        else:
            zeroes += 1
    if ones >= zeroes:  # ones dominant
        newlist = []
        for value in remaining:
            if value & mask == mask:
                newlist.append(value)
        remaining = newlist
    else:  # zeroes dominant
        newlist = []
        for value in remaining:
            if value & mask == 0:
                newlist.append(value)
        remaining = newlist
    if len(remaining) <= 1:
        break

print("remaining oxygen rate {}".format(remaining))


remaining2 = []
for row in lines:
    value = int(row, 2)
    remaining2.append(value)

for i in range(0, varlen):
    mask = 1 << (varlen-1-i)
    print("mask {} remaining {}".format(mask, remaining2))
    zeroes = 0
    ones = 0
    for value in remaining2:
        if value & mask == 0:
            zeroes += 1
        else:
            ones += 1
    if ones >= zeroes:  # less zeroes
        newlist = []
        for value in remaining2:
            if value & mask == 0:
                newlist.append(value)
        remaining2 = newlist
    else:  # less ones
        newlist = []
        for value in remaining2:
            if value & mask == mask:
                newlist.append(value)
        remaining2 = newlist
    if len(remaining2) <= 1:
        break

print("remaining co2 rate {}".format(remaining2))

print("soluce {}".format(remaining[0] * remaining2[0]))
