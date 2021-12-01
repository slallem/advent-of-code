#!/usr/bin/python3

import time
import re
import itertools
import copy

from typing import List


class Rule:
    index = -1
    value: str = None
    possibilities: List[List['Rule']]



def read_file(filename):
    global letterA
    global letterB
    res_rules = dict()
    res_messages = list()
    nb_lines = 0
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        text = line.strip()
        if len(text) == 0:
            # empty line
            pass
        else:
            # data line
            data = text.strip()
            nb_lines += 1

            if data[0] == "#":
                # ignore comments
                pass
            elif data[0] in "ab":
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
                        if valeurs[1] == "a":
                            letterA = clef
                        if valeurs[1] == "b":
                            letterB = clef
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

#def match_rule(rule_no: int, msg: str, verbose=False, tracing=False):


# def eval_series(prefix, keys: list):
#     res = prefix
#     if len(res) > 8:
#         return res
#     print("Trying series {}".format(keys))
#     for part in keys:  # 42 then 8 ...
#         print("Trying part {} of series {}".format(part, keys))
#         res = eval_rule(res, part)
#     return res

tmp = dict()
cnt = 0

def eval_rule(prefix: str, key: int, reentry=0):
    global cnt
    global tmp
    if reentry > 5:
        return prefix
    res = prefix
    # direct cases : "a" or "b"
    if key == letterA:
        res += "a"
        return res
    elif key == letterB:
        res += "b"
        return res
    # other cases (list of possiblities)
    alternatives = rules[key]
    # print("Alternatives for {} are {}".format(msg, alternatives))
    for alt in alternatives:
        cnt += 1
        tmp[cnt] = str()+prefix
        for idx in range(alt):  # 42 then 8 ...
            part = alt[idx]
            looping = reentry
            if part == key:
                looping += 1
            # tmp = eval_rule(tmp + "[{}]".format(part), part, looping)
            tmp[cnt] = eval_rule(tmp[cnt], part, looping)
            print("---partial discover {} index {}".format(tmp[cnt], idx))
        # End of serie
        tmp[cnt] = tmp[cnt] + "--EOF"
        print("For prefix \"{}\" i've found {}".format(prefix, tmp[cnt]))
    return res



start = time.time()

rules, messages = read_file('input-debug.txt')


for key in rules.keys():
    print("{} => {}".format(key, rules[key]))


print()
print("Part #1")
ok = 0
ko = 0
for message in messages:
    answer = eval_rule("", 0)
    # print("{} = {}".format(b_match, message))
    # if b_match:
    #     ok += 1
    # else:
    #     ko += 1

print(tmp)

print("total ok {} ko {}".format(ok, ko))

# PATCH PART2
rules[8] = [[42], [42, 8]]
rules[11] = [[42, 31], [42, 11, 31]]


# print()
# print()
# for key in rules.keys():
#     print("{} => {}".format(key, rules[key]))


# print()
# print("Part #2")
# ok = 0
# ko = 0
# for message in messages:
#     test = match_rule(0, message)
#     print("{} = {}".format(test, message))
#     if test:
#         ok += 1
#     else:
#         ko += 1
# print("total ok {} ko {}".format(ok, ko))
#
# print("{}".format(rules[8]))
#





end = time.time()
print("")
print("Done! in {:.3f} ms ".format((end - start)*1000))