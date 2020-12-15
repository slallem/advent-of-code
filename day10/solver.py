
import time
import re
import itertools


def regex_examples():
    sample = 'les années 1950 à 2000 couvrent 50 années de fooooolie'
    print(re.findall(r'([0-9]+)', sample))
    print(re.findall(r'(ANN)', sample, re.IGNORECASE))
    print(re.findall(r'(xyz)', sample))
    print(re.match(r'^(.+95)', sample) is not None)
    print(re.match(r'xyz', sample) is not None)


def minval(arr):
    res = arr[0]
    for val in arr:
        if val < res:
            res = val
    return res


def maxval(arr):
    res = arr[0]
    for val in arr:
        if val > res:
            res = val
    return res


def combinations(items: list, r: range = None):
    c = list()
    if r is None:
        r = range(1, len(items)+1)
    for i in r:
        c.extend(list(itertools.combinations(items, i)))
    return c


def decode_ligne(data):
    return int(data)


def read_file(filename):
    arr = list()
    nb_lines = 0
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        text = line.strip()
        if len(text) == 0:
            # empty line
            nb_lines += 0
        else:
            # data line
            data = text.strip()
            nb_lines += 1
            arr.append(decode_ligne(data))
    print("number of lines {}".format(nb_lines))
    return arr


start = time.time()

# regex_examples()
# print(combinations(["A", "B", "C"], range(2,3)))
# print(combinations(["X", "Y", "Z"]))



def find_suitable_chargers(inlist: list, joltage: int):
    res = list()
    remain = list()
    for v in inlist:
        difference = (v - joltage)
        if 0 <= difference <= 3:
            #print("{} match diff {} for j {}".format(v, difference, joltage))
            res.append(v)
        else:
            #print("{} NO match diff {} for j {}".format(v, difference, joltage))
            remain.append(v)
    inlist.clear()
    for v in remain:
        inlist.append(v)
    return res


def count_diffs(valeurs: list):
    diffs = dict()
    diffs[1] = 0
    diffs[2] = 0
    diffs[3] = 0
    for i in range(0, len(valeurs)):
        if i == 0:
            diff = valeurs[i]
        else:
            diff = valeurs[i] - valeurs[i-1]
        diffs[diff] = diffs[diff] + 1
        #print(".diff {} {} ".format(valeurs[i], diff))
    print("counters at end {}".format(diffs))
    print("claculus at end {}".format(diffs[1] * diffs[3]))


def resolve(l: list, joltage: int, stack: list):
    ads = l.copy()
    #print("resolve {} for j {}".format(len(ads), joltage))
    st = stack.copy()

    if len(ads) == 0:
        print("-->")
        print("chargers list exhausted.current output joltage {}, total {}".format(joltage, len(stack)))
        count_diffs(stack)
        print(stack)
        print("<--")

    suitables = find_suitable_chargers(ads, joltage)

    if len(suitables) == 0:
        #print("no more suitable chargers, remaining {} current output joltage {}".format(len(ads), joltage))
        return

    for ad in suitables:
        st.append(ad)
        still_available = l.copy()
        still_available.remove(ad)
        newjoltage = ad
        resolve(still_available, newjoltage, st.copy())


cache = dict()

def number_of_poss_to_get_exactly(ads: list, joltage: int):
    global cache
    res: int
    if joltage in cache.keys():
        return cache[joltage]
    if joltage < 0:
        res = 0
    elif joltage == 0:
        res = 1
    else:  # joltage > 0
        if joltage not in ads:
            res = 0
        else:
            res = 0
            res += number_of_poss_to_get_exactly(ads, joltage-1)
            res += number_of_poss_to_get_exactly(ads, joltage-2)
            res += number_of_poss_to_get_exactly(ads, joltage-3)

    cache[joltage] = res
    print("possibilities to get {} jolts is {}".format(joltage, res))
    return res

# def number_of_poss_to_get(ads: list, joltage: int):
#     return
#     for i in range(0, len(ads)-1):
#         possibilities = 0
#         poss = list()
#         if ()
#         for j in range(i+1, len(ads)):
#             diff = ads[j] - ads[i]
#             if 0 <= diff <= 3:
#                 possibilities += 1
#                 poss.append(ads[j])
#         print("step {:02d} val {} possibilities {} count {} / {} ".format(i, ads[i], poss, possibilities, possibilities-1))
#         if res == 0:
#             res = possibilities
#         else:
#             res = res * (possibilities-1)


def resolve2(l: list):
    # must be sorted
    ads = l.copy()
    ads.sort()
    ads.insert(0, 0)
    maxj = max(ads)
    res = 0
    #for i in range(len(ads)-1, 0, -1):
    for i in range(0, len(ads)-1):
        possibilities = 0
        poss = list()
        for j in range(i+1, len(ads)):
            diff = ads[j] - ads[i]
            if 0 <= diff <= 3:
                possibilities += 1
                poss.append(ads[j])
        print("step {:02d} val {} possibilities {} count {} / {} ".format(i, ads[i], poss, possibilities, possibilities-1))
        if res == 0:
            res = possibilities
        else:
            res = res * (possibilities-1)
    print("super mux = {}".format(res))




stack = list()
adapters = read_file('input.txt')
#adapters = [1, 2, 4]
my_adapter = max(adapters) + 3
adapters.append(my_adapter)

adapters.sort()
print("len {}: {}".format(len(adapters), adapters))



#resolve(adapters, 0, stack)

#resolve2(adapters)


print(number_of_poss_to_get_exactly(adapters, my_adapter))




end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))