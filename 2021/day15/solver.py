
# 2021 Day 15 part 1

from collections import Counter

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

#offsets = [
#    -storelen-1, -storelen, -storelen+1,
#             -1,             1,
#     storelen-1,  storelen,  storelen+1
#]
#offsets = [-storelen, -1, 1, storelen]
offsets = [storelen, 1] # down first

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
res = []

def explore(path, space, pos):
    global besttot
    global bestpath
    path[pos] = space[pos]
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

    if tot > besttot:
        # bad way
        return
    #print("evaluating pos {}, {}".format(pos % storelen, pos // storelen))
    if pos == exit_pos:
        #print("exit reached at {}".format(pos))
        print("exit reached at {}, {} = {}".format(pos % storelen, pos // storelen, tot))
        if tot <= besttot:
            besttot = tot
            bestpath = path
        res.append(tot)
        return
    voisins = dict()
    for offset in offsets:
        if (pos+offset) not in path.keys():
            if (pos+offset) in space.keys():
                voisins[pos+offset] = space[pos+offset]
    if not voisins:
        #print("bad way: dead end")
        return
    # explore min ways
    min_way = min(voisins.values())
    #print("min is {}".format(min_way))
    for v in voisins.keys():
        #if voisins[v] == min_way:
        #print(path)
        explore(path.copy(), space, v)


space = carte.copy()
explore(path, space, 0)

print("bestpath {} ".format(bestpath))
print(res)

# gives 811

