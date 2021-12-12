
# 2021 Day 12 part 1

import time

start = time.time()

f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()


def addCx(n,a,b):
    if a not in n.keys():
        n[a] = set()
    if b not in n.keys():
        n[b] = set()
    n[a].add(b)
    n[b].add(a)

nodes = dict()
for line in lines:
    if len(line) > 0:
        vals = line.strip().split("-")
        addCx(nodes, vals[0], vals[1])

print("{}".format(nodes))
print("{}".format(nodes.keys()))

results = []


def traverse(k, path, situation):
    newsit = situation.copy()
    doors = newsit[k]
    if k == 'end':  # exit reach = path complete !
        path.append(k)
        results.append(path)
        return
    if k == k.lower():  # cannot be visited twice
        del newsit[k]
    newpath = path.copy()
    newpath.append(k)
    for door in doors:
        if door in newsit.keys(): # else wrong way
            traverse(door, newpath, newsit)



# Explore the graph...
traverse('start', [], nodes.copy())


print("{}".format(results))
print("{}".format(len(results)))



end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))
