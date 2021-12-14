
# 2021 Day 14 part 2

# Pffff...

from collections import Counter

#f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

repl = dict()
poly = ""

for line in lines:
    if len(line) > 0:
        if "->" in line:
            vals = line.strip().split("->")
            pair = vals[0].strip()
            c2insert = vals[1].strip()
            repby = [ "" + pair[0] + c2insert, "" + c2insert + pair[1]]
            repl[pair] = repby
        else:
            if len(poly) == 0:
                poly = line.strip()

#print(poly)
#print(repl)

letterCounters = dict(Counter(poly))

def traite(pairCounter, lc):
    newcount = dict()
    for p in pairCounter.keys():
        nb = pairCounter[p]
        r1 = repl[p][0]
        r2 = repl[p][1]
        if r1 not in newcount.keys():
            newcount[r1] = 0
        if r2 not in newcount.keys():
            newcount[r2] = 0
        #print("{} => {} + {}".format(p,split1,split2))
        newcount[r1] += nb
        newcount[r2] += nb
        inserted_letter = repl[p][1][0]
        if inserted_letter not in lc.keys():
            lc[inserted_letter] = 0
        lc[inserted_letter] += nb
    return newcount

#print(lp)
#print(lp[0])

# poly to list of pairs
lp = list()
for i in range(0, len(poly)-1):
    lp.append(poly[i] + poly[i+1])

# list of pairs to aggregation (pair => count)
ag = dict(Counter(lp))

print("start: lettersCounter {} len {} pairs {}".format(letterCounters, sum(letterCounters.values()), ag))

#expected = [
#    "NCNBCHB",
#    "NBCCNBBBCBHCB",
#    "NBBBCNCCNBBNBNBBCHBHHBCHB",
#    "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"
#]

for iteration in range(0, 40):
    ag = traite(ag, letterCounters)
    #print(lp)
    #if iteration<6:
    #    print("iter {} ag {}".format(iteration+1, ag))
    #print("iter {} len {}".format(iteration+1, len(ag.keys())))
    #if iteration < len(expected):
    #    print()
    #    print("iter {} expect {} len {}".format(iteration+1, Counter(expected[iteration]), len(expected[iteration])))
    #    print("iter {} lettersCounter {} len {} pairs {}".format(iteration+1, letterCounters, sum(letterCounters.values()), ag))
    print("iter {} polymer length {}".format(iteration+1, sum(letterCounters.values())))


#print(ag)
#print(letterCounters)
#print("Res {}".format(res))

vmax = max(letterCounters.values())
vmin = min(letterCounters.values())

print("max {} min {} diff {}".format(vmax, vmin, vmax - vmin))

