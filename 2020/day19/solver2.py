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


# Globals
letterA = -1
letterB = -1


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


# regex_examples()
# print(combinations(["A", "B", "C"], range(2,3)))
# print(combinations(["X", "Y", "Z"]))
# -part2 is modified on entries 8: and 11: (loops)
# 8: 42 | 42 8
# 11: 42 31 | 42 11 31

def match_rule(rule_no: int, msg: str, verbose=False, tracing=False):
    res = internal_match_rule("", rule_no, msg, verbose, tracing)
    if verbose:
        print("avait {} a résolu {}".format(len(msg), res))
    return len(msg) == res


def internal_match_rule(come_from: str, rule_no: int, msg: str, verbose=False, tracing=False):
    come_from = "{}->{}".format(come_from, rule_no)
    if tracing:
        print(come_from)
    if verbose:
        print("Checking Rule {} remaining msg \"{}\"".format(rule_no, msg))
    if msg == "":
        if verbose:
            print("match impossible, epuisé")
        return -1
    if rule_no == letterA:
        if msg.startswith("a"):
            if verbose:
                print("match a")
            return 1
        else:
            if verbose:
                print("NO match a")
            return -1
    elif rule_no == letterB:
        if msg.startswith("b"):
            if verbose:
                print("match b")
            return 1
        else:
            if verbose:
                print("NO match b")
            return -1
    else: # sequence
        # if verbose:
        print("Complex : checking Rules {}".format(rules[rule_no]))
        for poss in rules[rule_no]:
            if tracing:
                print("ITER {} of {}".format(poss, rules[rule_no]))
            m = str()+msg
            # if verbose:
            #    print("  Complex : checking possibility of matching {}".format(poss))
            ok = True
            tot_cnt = 0
            for subrule_no in poss:
                if tracing:
                    print("  ITER2 {} of {}".format(subrule_no, poss))
                # if m == "":
                #     if verbose:
                #         print("Ici on s'attend a matcher la regle {} alors que msg épuisé".format(subrule_no))
                #     ok = False
                #     break
                cnt = internal_match_rule(come_from, subrule_no, m, verbose, tracing)
                if cnt > 0:
                    # match
                    m = m[cnt:]
                    tot_cnt += cnt
                else:
                    # no match, try another one
                    if tracing:
                        print("=Nomatch")
                    ok = False
                    break
            if ok:
                # and len(msg) == tot_cnt:
                if verbose or tracing:
                    print("On a trouvé {} qui matche parfaitement, reste{}-{}={}".format(poss, len(msg), tot_cnt, len(msg) - tot_cnt))
                return tot_cnt
        if verbose:
            print("Aucun ne match")
        return -1  # arrivé ici = aucun match trouvé


# print()
# possibilities = dict()
# for key in rules.keys():
#     poss = find_possibilities(key)
#     #print("{} => {}".format(key, poss))
#     print("{} => {}".format(key, len(poss)))


# Vérification si optim possible sur LIST vs SET = a priori nope
# p8 = find_possibilities(8)
# print("{} => {}".format(8, p8))
# s = set()
# for p in p8:
#     s.add(p)
# print("list is {} set is {}".format(len(p8), len(s)))


# print("{} => {}".format(11, find_possibilities(11)))

# TU
#cas simples
#10: 39 20 | 39 39 => 10: ab ou aa

# print(match_rule(10, "aa", 0, mx)) # OK
#print(match_rule(10, "bb", 0, mx)) # KO
#print(match_rule(10, "ab", 0, mx)) # OK
#print(match_rule(0, "aabaabbaabbbabababbababa", 0, mx, verbose=True)) # OK (etait OK en Part1)
#print(match_rule(0, "babbabbabbbaaaaaaabbabba", 0, mx)) # KO (était KO en Part1)




start = time.time()

rules, messages = read_file('input.txt')
#rules, messages = read_file('input-debug2.txt')
#rules, messages = read_file('input-debug2.txt')
#rules, messages = read_file('input-debug.txt')

# print(match_rule(0, "aaaabbb", True))  # exemple part1 = ne doit pas marcher
#print(match_rule(0, "ababbb", True))  # exemple part1 = doit marcher
# exit(99)

# print()
# print("Part #1")
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

# PATCH PART2
rules[8] = [[42], [42, 8]]
rules[11] = [[42, 31], [42, 11, 31]]



print()
print("Part #2")
ok = 0
ko = 0
for message in messages:
    test = match_rule(0, message)
    print("{} = {}".format(test, message))
    if test:
        ok += 1
    else:
        ko += 1
print("total ok {} ko {}".format(ok, ko))

print("{}".format(rules[8]))

print()
print()
print()
#print(match_rule(0, "abababaa", verbose=False, tracing=True))  # exemple debug = doit matcher en theorie

# print(match_rule(0, "aabb", verbose=False, tracing=True))  # exemple debug = doit matcher en theorie





end = time.time()
print("")
print("Done! in {:.3f} ms ".format((end - start)*1000))