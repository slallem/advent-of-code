
# 2021 Day 15 part 2

from collections import Counter
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
newcarte = dict()
factor = 5
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
                #print("copy {},{} -> {},{}".format(i, j, newx, newy))
carte = newcarte
hh = hh * factor
ww = ww * factor

offsets = [storelen, 1]  # down first

#determine reference score
refpath = dict()
for i in range(1, ww):
    refpath[i] = carte[i]
for j in range(1, hh):
    refpath[(storelen*j)+ww-1] = carte[(storelen*j)+ww-1]
refscore = sum(refpath.values())

best_score_at = dict()

path = dict()
bestpath = dict()
besttot = refscore

print("refscore is {}".format(refscore))

exit_pos = (storelen*(hh-1))+(ww-1)

explorations = []

def explore(path, pos):
    global besttot
    global bestpath
    path[pos] = carte[pos]
    tot = sum(path.values()) - path[0]

    # calculate cost to reach this point
    # then update (if best) or prune (if worst)
    if pos in best_score_at.keys():
        if tot < best_score_at[pos]:  # best or equal?
            best_score_at[pos] = tot
        else:  # worst = do not explore this way
            return
    else:
        best_score_at[pos] = tot

    #print("evaluating pos {}, {}".format(pos % storelen, pos // storelen))
    if pos == exit_pos:
        print("exit reached at {}, {} = {}".format(pos % storelen, pos // storelen, tot))
        if tot <= besttot:
            besttot = tot
            bestpath = path
        return

    if tot >= besttot:
        # bad way
        return

    voisins = dict()
    for offset in offsets:
        #if (pos+offset) not in path.keys():
        if (pos+offset) in carte.keys():
            voisins[pos+offset] = carte[pos+offset]
    #if not voisins:
    #    return
    for v in voisins.keys():
        explorations.append({'path': path.copy(), 'pos': v})


explorations.append({'path': path, 'pos': 0})

while len(explorations) > 0:
    exploration = explorations.pop()
    explore(exploration['path'], exploration['pos'])

print("bestpath {} ".format(bestpath))
print(res)

end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))
