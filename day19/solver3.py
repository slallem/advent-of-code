#!/usr/bin/python3

import time
import re
import itertools
import copy

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


def eval_series(keys: list, msg: str):
    # [42,8,..]
    remains = str()+msg
    print(keys)
    for part in keys:  # 42 then 8 ...
        print(part)
        match, remains = eval_rule(part, remains)
        if not match:
            # no match, try another one
            return False, remains
        # else continue the series til its end
    return True, remains


def eval_rule(key: int, msg: str):
    # direct cases : "a" or "b"
    if key == letterA:
        if msg.startswith("a"):
            return True, msg[1:]
        else:
            return False, msg
    elif key == letterB:
        if msg.startswith("b"):
            return True, msg[1:]
        else:
            return False, msg
    # other cases (list of possiblities)
    alternatives = rules[key]
    for series in alternatives:
        match, remains = eval_series(series, msg)
        if match and remains == "":
            # found perfect match
            return True, ""


start = time.time()

rules, messages = read_file('input.txt')


# for key in rules.keys():
#     print("{} => {}".format(key, rules[key]))
#

print()
print("Part #1")
ok = 0
ko = 0
for message in messages:
    b_match, b_remains = eval_rule(0, message)
    # print("{} = {}".format(test, message))
    if b_match:
        ok += 1
    else:
        ko += 1
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