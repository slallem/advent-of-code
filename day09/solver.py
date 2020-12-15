
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


def combinations(items: list, r: range = None):
    c = list()
    if r is None:
        r = range(1, len(items)+1)
    for i in r:
        c.extend(list(itertools.combinations(items, i)))
    return c

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


values = list()

def decode_ligne(data):
    values.append(int(data))
    #print("data {}".format(values))


def do_the_job(filename):
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
            decode_ligne(data)
    print("number of lines {}".format(nb_lines))


start = time.time()

# regex_examples()
do_the_job('input.txt')
# print(combinations(["A", "B", "C"], range(2,3)))
# print(combinations(["X", "Y", "Z"]))

print(len(values))

tot = len(values)

def get_sum(arr: list, value: int):
    #combi = combinations(arr,2)
    combi = list(itertools.combinations(arr, 2))
    for c in combi:
        if c[0] + c[1] == value:
            return c
    return None


# soluce1 = 85848519
#
# for i in range(25, tot):
#     arr = values[i-25:i]
#     current = values[i]
#     print("index {} : value {} : ".format(i, current), end="")
#     sum = get_sum(arr, current)
#     if sum is None:
#         print("*** is not valid".format(i, current))
#         break
#     else:
#         print("OK = ".format(i, current))


soluce1 = 85848519

# for r in range(len(values), 2, -1):
#     combis = combinations(values, range(r))
#     for c in combis:
#         sum = 0
#         for cv in c:
#             sum += cv
#         if sum == soluce1:
#             print("{} matches".format(c))
#             break

def ismatch(arr: list):
    sum = 0
    for index in range(len(arr)):
        sum += arr[index]
        if sum == soluce1:
            res = arr[:index]
            print("sum of {} is {}".format(res, soluce1))
            # min = res[0]
            # max = res[0]
            # for val in res:
            #     if val > max:
            #         max = val
            #     if val < min:
            #         min = val
            mi = minval(res)
            ma = maxval(res)
            print("sum of {} plus {} is {}".format(mi, ma, mi+ma))
            return res
        if sum > soluce1:
            break
    return None


for i in range(tot):
    res = ismatch(values[i:tot])
    if res is not None:
        print(res)
        print(res[0] + res[-1])
        break

print("done")

end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))


