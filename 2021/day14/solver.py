
# 2021 Day 14 part 1

from collections import Counter

#f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

repl = []
poly = ""

for line in lines:
    if len(line) > 0:
        if "->" in line:
            vals = line.strip().split("->")
            repl.append([list(vals[0].strip()), vals[1].strip()])
        else:
            if len(poly) == 0:
                poly = line.strip()

print(poly)
print(repl)


def traite(apoly):
    newpoly = ""
    for i in range(0, len(apoly)-1):
        newpoly += apoly[i]
        for r in repl:
            if apoly[i] == r[0][0] and apoly[i+1] == r[0][1]:
                #print("match {}{}".format(lpoly[i],lpoly[i+1]))
                newpoly += r[1]
                break
    newpoly += apoly[len(apoly)-1]
    return newpoly

#print(lp)
#print(lp[0])


lp = "" + poly

for iteration in range(0, 10):
    lp = traite(lp)
    #if iteration < 3:
    #    print(lp)
    print("iter {} len {}".format(iteration+1, len(lp)))


res = Counter(lp)
print(res)
vmax = max(res.values())
vmin = min(res.values())
print(vmax - vmin)

