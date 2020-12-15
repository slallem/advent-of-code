
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
    res = list(data)
    #print("data {}".format(chars))
    return res


def read_file(filename):
    res = list()
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
            res.append(decode_ligne(data))
    #print("number of lines {}".format(nb_lines))
    return res


start = time.time()

# regex_examples()
# print(combinations(["A", "B", "C"], range(2,3)))
# print(combinations(["X", "Y", "Z"]))
#read_file('input.txt')

timestamp = 1000390
buses = "23,x,x,x,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,383,x,x,x,x,x,x,x,x,x,x,x,x,13,17,x,x,x,x,19,x,x,x,x,x,x,x,x,x,29,x,503,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,37"

# timestamp = 939
#buses = "7,13,x,x,59,x,31,19"


# # part1

# nearestbus = -1
# buscount = 0
# bestpassage = 0
# for busid in busids:
#     if busid != "x":
#         numbus = int(busid)
#         buscount += 1
#         modulo = (timestamp % numbus)
#         nextpassage = timestamp - modulo + numbus
#         print("-- bus ID {} next passage {} modulo {}".format(numbus, nextpassage, modulo))
#         if nearestbus < 0:
#             nearestbus = numbus
#             bestpassage = nextpassage
#         if nextpassage < bestpassage:
#             nearestbus = numbus
#             bestpassage = nextpassage
#
# print("bus ID {} next passage {} time to wait {} soluce {}".format(nearestbus, bestpassage, bestpassage-timestamp, (bestpassage-timestamp)*nearestbus))


buses = "67,7,59,61"
buses = "67,7,x,59,61"
buses = "1789,37,47,1889"
buses = "23,x,x,x,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,383,x,x,x,x,x,x,x,x,x,x,x,x,13,17,x,x,x,x,19,x,x,x,x,x,x,x,x,x,29,x,503,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,37"
buses = "17,x,13,19"
busids = buses.split(",")

data = list()
offsets = list()

print()
# part2
offset = -1
maxbus =  0
maxbus_offset = 0
for busid in busids:
    offset += 1
    if busid != "x":
        numbus = int(busid)
        if numbus > maxbus:
            maxbus = numbus
            maxbus_offset = offset
        data.append(numbus)
        offsets.append(offset)
        print("-- bus ID {} offset {}".format(numbus, offset))



# data =    [23, 41, 383, 13, 17, 19, 29, 503, 37]
# offsets = [0,  13,  23, 36, 37, 42, 52, 54,  91]

# data = [13, 17, 19, 23, 29, 37, 41, 383, 503]
# offsets = [36, 37, 42, 0,  52, 91, 13,  23,  54]

print("max bus is {} and its offset is {}".format(maxbus, maxbus_offset))
print("{}".format(data))
print("{}".format(offsets))


def eval(ts, verbose=True, header=True):
    matching = 0
    if header:
        print("testing {} ... ".format(ts), end="")
    for i in range(len(data)):
        bus = data[i]
        modulo = ts % bus
        nextpassage = ts - modulo + bus
        # nextpassage_offset = nextpassage - ts
        next_passage_offset = (bus - modulo) % bus
        if verbose:
            print()
            print("  bus {} modulo {} next_passage {} with offset {} expected {}... ".format(
                    data[i], modulo, ts + next_passage_offset, next_passage_offset, offsets[i]), end="")
        if next_passage_offset == offsets[i]:
            matching += 1
            # print("!!! match for {} found at {}".format(bus, ts))
            # break
        # else:
        #     break
    #if matching > 0:
    if header:
        print("matching {} ".format(matching))
    return 0 #matching


# print(eval(1068781))
# print(eval(3417, True))
# exit(0)

# [23, 41, 383, 13, 17, 19, 29, 503, 37]
# [0, 13, 23, 36, 37, 42, 52, 54, 91]

z = 0
#z = 15122417
# z = 3119513
# z = 3857876250 #383
# z = 3999868521 #503
# z = 4052669437
# z = 4097617014 ##383 and 503 match
# z = 5053541352
# z = 9944321515 #  383 * 503 * 23
# z = 226634375523 # *41
# z = 534743315395
# z = 11664997100264
# z = 20736770697816

ts = 0
incr = 1
stop_at = 1

# z = 19872
# incr = 23 * 41
# stopat = 3
#
# z = 44529472
# incr = 23 * 41 * 383
# stopat = 4

# z = 56714834924
# incr = 41 * 383 * 23 *
# stopat = 4

while True:
    ts += incr
    matching = eval(ts, False, False)
    if matching >= stop_at:
        print(eval(ts, True, True))
        exit(0)
    if matching == len(data):  # all matching !!
        print("all match! {} ".format(ts))
        exit(0)
    # if z > 800000:
    #     break


# print("bus ID {} next passage {} time to wait {} soluce {}".format(nearestbus, bestpassage, bestpassage-timestamp, (bestpassage-timestamp)*nearestbus))




end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))