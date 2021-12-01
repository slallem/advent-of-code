#!/usr/bin/python3

import time
import re
import itertools
import copy


def regex_examples():
    sample = 'les années 1950 à 2000 couvrent 50 années de fooooolie'
    print(re.findall(r'([0-9]+)', sample))
    print(re.findall(r'(ANN)', sample, re.IGNORECASE))
    print(re.findall(r'(xyz)', sample))
    print(re.match(r'^(.+95)', sample) is not None)
    print(re.match(r'xyz', sample) is not None)
    print(re.match(r'^([ a-z0-9^:]+):.([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)$', "departure date: 41-532 or 552-956").groups())


def combinations(items: list, r: range = None):
    c = list()
    if r is None:
        r = range(1, len(items)+1)
    for i in r:
        c.extend(list(itertools.combinations(items, i)))
    return c


def read_file(filename):
    res_rules = dict()
    res_messages = list()
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

            if data[0] in "ab":
                # ababbb
                # bababa
                # abbbab...
                res_messages.append(data)
            else:
                # 4: "a"
                # 121: 20 64 | 39 92
                match = re.match(r'^([0-9]+): (.*)$', data)
                if match is not None:
                    grp = match.groups()
                    clef = int(grp[0])
                    valeurs = grp[1]
                    rule = list()  # heterogeneous list of values "a" or [[12 5],...]
                    if valeurs[0] == '"':
                        rule.append(valeurs[1])  # possibilities = [ "a" ]
                    else:
                        for rule_set in valeurs.split("|"):
                            vv = list()
                            for vvv in re.findall(r'([0-9]+)', rule_set):
                                vv.append(int(vvv))
                            rule.append(vv)
                    res_rules[clef] = rule
                else:
                    raise Exception("ERREUR impossible de décoder {}".format(data))
    return res_rules, res_messages


start = time.time()

# regex_examples()
# print(combinations(["A", "B", "C"], range(2,3)))
# print(combinations(["X", "Y", "Z"]))

rules, messages = read_file('input.txt')

cache = dict()


def find_possibilities(key: int):
    if key in cache.keys():
        return cache[key]
    res = list()
    val = rules[key]
    for level1 in val:
        if isinstance(level1, str):
            # str
            res.append(level1)
        else:
            # list of integers
            chaine = ""
            if len(level1) == 1:
                # 1 combi seule 8 => [42]
                res.extend(find_possibilities(level1[0]))
            else:
                # 2 combis
                gauche = find_possibilities(level1[0])
                droite = find_possibilities(level1[1])
                for g in gauche:
                    for d in droite:
                        mix = "{}{}".format(g,d)
                        res.append(mix)
    cache[key] = res
    return res


print()
remains = copy.deepcopy(rules)
possibilities = dict()
for key in rules.keys():
    poss = find_possibilities(key)
    #print("{} => {}".format(key, poss))
    print("{} => {}".format(key, len(poss)))

print()
ok = 0
ko = 0
poss = find_possibilities(0)
for message in messages:
    print("{} = {}".format(message in poss, message))
    if message in poss:
        ok += 1
    else:
        ko += 1


print("total ok {} ko {}".format(ok, ko))

end = time.time()
print("")
print("Done! in {:.3f} ms ".format((end - start)*1000))