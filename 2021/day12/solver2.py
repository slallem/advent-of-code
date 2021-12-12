
# 2021 Day 12 part 2

# Bonne résolution #1 : Eviter de se coucher à 3h30 du mat
# Bonne résolution #2 : Eviter l'abus de vin de Savoie (le Pomerol va aussi bien sur la raclette)
# Bonne résolution #3 : Arrêter de se lever à 6h
# Bonne résolution #4 : C'est dimanche, je retourne me coucher !!!

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

results = set()


def traverse(k, path, situation, allow):
    newsit = situation.copy()
    doors = newsit[k]

    if k == 'end':  # exit reach = path complete !
        path.append(k)
        results.add(",".join(path))
        return

    newpath = path.copy()
    newpath.append(k)

    if k == 'start':
        del newsit[k]
    elif k == k.lower():
        if k == allow:
            if k in path: # allows once befor del == allow twice per small
                del newsit[k]
        else:
            del newsit[k]

    #print(path)

    for door in doors:
        if door in newsit.keys():  # else wrong way
            traverse(door, newpath, newsit, allow)

# Explore the graph...
for cave in nodes.keys():
    if cave == cave.lower() and cave not in ['start', 'end']:
        traverse('start', [], nodes.copy(), cave)

#for res in results:
#    print("{}".format(res))
print("{}".format(len(results)))



end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))
