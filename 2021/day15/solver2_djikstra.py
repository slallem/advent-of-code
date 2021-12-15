
# 2021 Day 15 part 2 (refacto)
# Rewritten using oriented graph solving algorithm

# Djikstra
# Ran in 1376s (~23mn)

# => 3019 = wrong ??? (too high)
# Try
# => 3019-8 (start) = 3011 = wrong (too low)
# I can't see why it doesn't work, as it works fine with given examples
# Other tries in-between (as I know it is somewhere in 3011 > ? > 3019)
# => expected answer was 3012

#FIXME
# Need to find out why result is 3019 instead of 3012

import time

start = time.time()

#f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

storelen = 1000

ww = 0
hh = 0
carte = dict()
for line in lines:
    if len(line) > 0:
        ww = 0
        for car in line.strip():
            carte[(storelen * hh) + ww] = int(car)
            ww += 1
        hh += 1

# Step #2: extend map
factor = 5
newcarte = dict()
for extent_y in range(0, factor):
    for extent_x in range(0, factor):
        increment = extent_x + extent_y
        for i in range(0, ww):
            for j in range(0, hh):
                pos = (j * storelen) + i
                newx = i + (extent_x * ww)
                newy = j + (extent_y * hh)
                newpos = (newy * storelen) + newx
                newval = ((carte[pos] + increment - 1) % 9) + 1
                newcarte[newpos] = newval

carte = newcarte
hh = hh * factor
ww = ww * factor

print("Solving graph size {}x{}...".format(ww,hh))

# dijkstra algorithm taken from
# https://www.it-swarm-fr.com/fr/python/lalgorithme-de-dijkstra-en-python/1046618165/

nodes = carte.keys()
distances = dict()
for node in nodes:
    voisins = {}
    for offset in [1, storelen]:
        if (node+offset) in nodes:
            voisins[node+offset] = carte[node+offset]
    distances[node] = voisins

# print(nodes)
# print(distances)

# Example of use:
# nodes = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
# distances = {
#     'B': {'A': 5, 'D': 1, 'G': 2},
#     'A': {'B': 5, 'D': 3, 'E': 12, 'F': 5},
#     'D': {'B': 1, 'G': 1, 'E': 1, 'A': 3},
#     'G': {'B': 2, 'D': 1, 'C': 2},
#     'C': {'G': 2, 'E': 1, 'F': 16},
#     'E': {'A': 12, 'D': 1, 'C': 1, 'F': 2},
#     'F': {'A': 5, 'E': 2, 'C': 16}}

unvisited = {node: None for node in nodes}  # using None as +inf
visited = {}
current = 0  # Starting point
currentDistance = 0
unvisited[current] = currentDistance

i = 0
while True:
    for neighbour, distance in distances[current].items():
        if neighbour not in unvisited:
            continue
        newDistance = currentDistance + distance
        if unvisited[neighbour] is None or unvisited[neighbour] > newDistance:
            unvisited[neighbour] = newDistance
    visited[current] = currentDistance
    del unvisited[current]
    if not unvisited:
        break
    candidates = [node for node in unvisited.items() if node[1]]
    current, currentDistance = sorted(candidates, key=lambda x: x[1])[0]
    i += 1
    if i % 1000 == 0:  # Display progression
        print("{:.2f}% : remaining {} of {}".format(100-(len(unvisited)*100/len(nodes)), len(unvisited), len(nodes)))

# print(visited)
print(visited[((hh-1)*storelen)+ww-1])


end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))
