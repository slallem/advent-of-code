#!/usr/bin/python3

import time
import re
import itertools
from itertools import permutations


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


def decode_ligne(data):
    res = list(data)
    #print("data {}".format(chars))
    return res


rule_range1 = dict()
rule_range2 = dict()

depkeys = set()
tickets = list()

def read_file(filename):
    section = 0
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
            if section == 0:  #rules
                if data == "your ticket:":
                    section = 1
                else:
                    fields = re.match(r'^([ a-z0-9^:]+):.([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)$', data).groups()
                    print("fields {}".format(fields))
                    if "departure" in fields[0]:
                        depkeys.add(fields[0])
                    rule_range1[fields[0]] = range(int(fields[1]), int(fields[2])+1)
                    rule_range2[fields[0]] = range(int(fields[3]), int(fields[4])+1)
            else:
                if "," in data:
                    values = data.split(",")
                    t = list()
                    for v in values:
                        t.append(int(v))
                    tickets.append(t)
            res.append(decode_ligne(data))
    return res


start = time.time()

#regex_examples()
# print(combinations(["A", "B", "C"], range(2,3)))
# print(combinations(["X", "Y", "Z"]))

lines = read_file('input.txt')

#print(re.match(r'^([ a-z0-9^:]+):.([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)$', "departure date: 41-532 or 552-956").groups())


print("{}".format(rule_range1))
print("{}".format(rule_range2))
print("{}".format(tickets))



soluce = 0
valid_tickets = list()

total = 0
total_invalid = 0
for i in range(1, len(tickets)):
    total += 1
    tinvalid = 0
    for v in tickets[i]:
        valid_rules = 0
        for k in rule_range1.keys():
            #print("test {} in {} = {}".format(v, rule_range1[k], v in rule_range1[k]))
            #print("test {} in {} = {}".format(v, rule_range2[k], v in rule_range2[k]))
            if v in rule_range1[k] or v in rule_range2[k]:
                valid_rules += 1
                break
        if valid_rules == 0:
            print("ticket {} is not valid because of {} validrules {}".format(tickets[i], v, valid_rules))
            #print("invalid {} ".format(v), end="")
            total_invalid += 1
            tinvalid += 1
            soluce += v
            break
    if tinvalid == 0:
        valid_tickets.append(tickets[i])



def validfor(akey, exclude):
    res = list()
    for i in range(len(valid_tickets[0])):
        invalid = 0
        if i not in exclude:
            for t in valid_tickets:
                v = t[i]
                if v not in rule_range1[akey] and v not in rule_range2[akey]:
                    invalid += 1
                    break
            if invalid == 0:
                #print("{} index is probably {}".format(akey, i))
                res.append(i)
    return res


print("soluce {} tickts {} invalid {}".format(soluce, total, total_invalid))
#print("valid tickts {}".format(valid_tickets))


print("depkeys {}".format(depkeys))

#for x in permutations(depkeys):
#    print("combi {}".format(x))

clefs = list(rule_range1.keys())
exclude = [11, 12, 4, 5, 17, 16, 1, 2,
           18, 6, 14, 3]
for clef in ["arrival platform", "zone", "arrival track", "train", "seat", "arrival station", "type", "route",
             "departure time", "departure date", "departure location", "departure station"]:
    clefs.remove(clef)

for k in clefs:
    valids = validfor(k, exclude)
    print("{} is possibly {}".format(k, valids))

mt = tickets[0]
print(mt[13]*mt[15]*mt[3]*mt[18]*mt[6]*mt[14])

# beurk un peu trop manuel mais ça a fait le job...
# tout cela aurait mérité d'être automatisé surtout s'il y avait eu plus de champs

#for t in valid_tickets:


end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))