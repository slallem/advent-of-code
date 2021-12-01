
# 2021 Day 1 part 1

values = []
f = open('input.txt', 'r')
lines = f.readlines()

for row in lines:
    values.append(int(row))

freqs = set()
nbval = len(values)
lo = 0
hi = 0
same = 0
ref = values[0]

for i in range(1, nbval):
    if values[i] < ref:
        lo = lo + 1
    elif values[i] > ref:
        hi = hi + 1
    else:
        same = same + 1
    ref = values[i]

print("lo {} hi {} same {}".format(lo, hi, same))
