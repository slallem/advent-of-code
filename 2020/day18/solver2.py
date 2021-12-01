#!/usr/bin/python3

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
    print(re.match(r'^([ a-z0-9^:]+):.([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)$', "departure date: 41-532 or 552-956").groups())


def combinations(items: list, r: range = None):
    c = list()
    if r is None:
        r = range(1, len(items)+1)
    for i in r:
        c.extend(list(itertools.combinations(items, i)))
    return c


def decode_ligne(data):
    #res = list(data)
    #print("data {}".format(chars))
    return data


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
    return res


def evaluate(expr: str, verbose: bool=False):
    chars = list(expr.replace(" ", ""))
    if verbose:
        print("Evaluating {}".format(chars))
    stack = list()
    chaine = ""
    for char in chars:
        if verbose:
            print("- Caractère {} : ".format(char), end="")
        if char in "0123456789+*":
            if verbose:
                print("= added {}".format(char))
            chaine += char
        elif char == "(":
            if verbose:
                print("= new group".format())
            stack.append(chaine)
            pass
        elif char == ")":
            if verbose:
                print("= end of group, expr = {}".format(chaine))
            stack.append(chaine)
            chaine = ""
        else:
            raise Exception("Symbole inattendu {}".format(char))
    return 0


# def custom_eval(expr: str, verbose: bool=False):
#     # Force + priority
#     xp = expr.replace(" ", "")
#     if verbose:
#         print("Custom eval of {}".format(xp))
#     while True:
#         match = re.match(r'(.*)([0-9]+[+][0-9]+)(.*)$', xp)
#         if match is not None:
#             groupes = match.groups()
#             if verbose:
#                 print("groupes  = {}".format(groupes))
#             if len(groupes) == 3:
#                 xp = groupes[0] + str(eval(groupes[1])) + groupes[2]
#                 if verbose:
#                     print("new expr = {}".format(xp))
#         else:
#             if verbose:
#                 print("No match for +")
#             break
#     return eval(xp)


def custom_eval(expr: str, verbose: bool=False):
    xp = expr.replace(" ", "")
    #xp = xp.replace("+", "+ ")
    #xp = xp.replace("*", " * ")
    items = re.findall(r"[+0-9]+|[*]", xp)
    if verbose:
        print("After Préfiltre eval = {}".format(items))
    xp2 = ""
    for item in items:
        if "+" in item:
            xp2 += str(eval(item))
        else:
            xp2 += item
    return eval(xp2)



def eval_ligne(expression, verbose: bool = False):
    res = expression.replace(" ", "")
    if verbose:
        print("Start expr = {}".format(res))
    while True:
        match = re.match(r'^(.*)[(]([0-9]+[\\*+0-9]*[0-9]+)[)](.*)$', res)
        if match is not None:
            groupes = match.groups()
            if verbose:
                print("groupes  = {}".format(groupes))
            if len(groupes) == 3:
                res = groupes[0] + str(custom_eval(groupes[1])) + groupes[2]
                if verbose:
                    print("new expr = {}".format(res))
        else:
            if verbose:
                print("No match for parenthesis")
            break
    res = custom_eval(res, verbose)
    print("Last result = {}".format(res))
    return res


start = time.time()

# regex_examples()
# print(combinations(["A", "B", "C"], range(2,3)))
# print(combinations(["X", "Y", "Z"]))

lines = read_file('input.txt')

# print("number of lines {}".format(len(lines)))

# # print(evaluate(expr="1 + (2 * 3) + (4 * (5 + 6))", verbose=True))
# expr = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
# print("{}".format(expr))

#groupes = re.match(r'^(.*)(\\([\\+*0-9\\^\\(^\\)]))(.*)$', expr).groups()

#print(eval_ligne(expression="2 * 3 + (4 * 5)", verbose=True))
#print(eval_ligne(expression="2 * 3 + (4 * 5)", verbose=True))

#print(custom_eval("2+1+5*5", True))

# TU
print(eval_ligne(expression="1 + (2 * 3) + (4 * (5 + 6))", verbose=False))
print(eval_ligne(expression="2 * 3 + (4 * 5)", verbose=False))
print(eval_ligne(expression="5 + (8 * 3 + 9 + 3 * 4 * 3)", verbose=False))
print(eval_ligne(expression="5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", verbose=False))
print(eval_ligne(expression="((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", verbose=False))


total = 0
for line in lines:
    total += eval_ligne(line)

print("number of lines {}, Part #1 total {}".format(len(lines), total))

end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))