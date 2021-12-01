
# 2021 Day 1 part 2

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

for i in range(3, nbval):
    ref0 = values[i-3]+values[i-2]+values[i-1]
    ref1 = values[i-2]+values[i-1]+values[i]
    if ref1 < ref0:
        lo = lo + 1
    elif ref1 > ref0:
        hi = hi + 1
    else:
        same = same + 1

print("lo {} hi {} same {}".format(lo, hi, same))
