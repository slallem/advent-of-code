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

class Product:
    ingredients = set()
    allergens = set()

#For part2
# excluded = ["nuts", "gnrpml", "wheat", "jxh" ]
excluded = []


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
            p = Product()
            # (contains fish, wheat)
            grp = re.match(r'^(.+) [(]contains (.+)[)]$', data).groups()
            left = grp[0]
            right = grp[1]
            p.ingredients = set()
            for s in left.split(" "):
                p.ingredients.add(s)
                for ex in excluded:
                    if ex in p.ingredients:
                        p.ingredients.remove(ex)
            p.allergens = set()
            for s in right.split(","):
                p.allergens.add(s.strip())
                for ex in excluded:
                    if ex in p.allergens:
                        p.allergens.remove(ex)
            res.append(p)
    return res


start = time.time()

# regex_examples()
# print(combinations(["A", "B", "C"], range(2,3)))
# print(combinations(["X", "Y", "Z"]))

products = read_file('input.txt')

# for product in products:
#     print("{} = {}".format(product.ingredients, product.allergens))

all_allergens = dict()
for product in products:
    for a in product.allergens:
        if a in all_allergens.keys():
            all_allergens[a] += 1
        else:
            all_allergens[a] = 1

all_ingredients = dict()
for product in products:
    for i in product.ingredients:
        if i in all_ingredients.keys():
            all_ingredients[i] += 1
        else:
            all_ingredients[i] = 1

print("ingredients {} , allergens {}".format(len(all_ingredients), len(all_allergens)))

allergen_counters = dict()
for i in all_ingredients.keys():
    d = dict()
    for p in products:
        if i in p.ingredients:
            for a in p.allergens:
                if a in d.keys():
                    d[a] += 1
                else:
                    d[a] = 1
    allergen_counters[i] = d
print("Allergen counters {}".format(allergen_counters))

allergenics = set()
possible_sources = dict()
for a in all_allergens.keys():
    poss = set()
    for p in products:
        if a in p.allergens:
            for i in p.ingredients:
                poss.add(i)
                allergenics.add(i)
    possible_sources[a] = poss

print("Possible sources {}".format(possible_sources))
print("Possible sources (flattened) {}".format(allergenics))

#PART 1


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


surely_allergenic = set()
for a in all_allergens.keys():
    products_that_contains = list()
    for p in products:
        if a in p.allergens:
            products_that_contains.append(p)
    bad_ingredients = list(products_that_contains[0].ingredients)  # liste à réduire
    for idx in range(1, len(products_that_contains)):
        bad_ingredients = intersection(bad_ingredients, products_that_contains[idx].ingredients)
    print("allergen {} => {}".format(a, bad_ingredients))
    for bi in bad_ingredients:
        surely_allergenic.add(bi)
print("Really bad ingredients = {}".format(surely_allergenic))

print("No allergens:")

tot = 0
safe_ingredients = set()
for a in all_ingredients.keys():
    if a not in surely_allergenic:
        safe_ingredients.add(a)
        print("{}", a, all_ingredients[a])
        tot += all_ingredients[a]

print("TOTAL {}", tot)

print("Safe ingradients {}", safe_ingredients)

# print("{} = {}".format(product.ingredients, product.allergens))

# part 2
# l = list(surely_allergenic)
# l.sort()
# for bi in l:
#     print("{} = {}".format(bi, allergen_counters[bi]))

# rdfr = {'peanuts': 9, 'dairy': 10, 'nuts': 14, 'eggs': 10, 'sesame': 11, 'wheat': 8, 'fish': 7, 'soy': 11}
# rfmvh = {'eggs': 8, 'sesame': 11, 'nuts': 14, 'wheat': 8, 'fish': 9, 'dairy': 8, 'soy': 8, 'peanuts': 7}
# xrmxxvn = {'peanuts': 10, 'dairy': 6, 'nuts': 14, 'eggs': 9, 'sesame': 10, 'wheat': 7, 'fish': 7, 'soy': 10}
# qxfzc = {'peanuts': 9, 'dairy': 9, 'nuts': 13, 'eggs': 10, 'sesame': 11, 'wheat': 8, 'fish': 9, 'soy': 10}
# jxh = {'peanuts': 8, 'dairy': 9, 'nuts': 11, 'eggs': 8, 'sesame': 7, 'wheat': 9, 'fish': 6, 'soy': 9}
# gnrpml = {'peanuts': 10, 'dairy': 10, 'nuts': 15, 'eggs': 9, 'sesame': 10, 'wheat': 9, 'fish': 9, 'soy': 11}
# vmhqr = {'peanuts': 8, 'dairy': 10, 'nuts': 13, 'eggs': 9, 'sesame': 10, 'wheat': 7, 'soy': 8, 'fish': 7}
# khpdjv = {'peanuts': 9, 'dairy': 8, 'nuts': 11, 'fish': 9, 'wheat': 7, 'soy': 10, 'sesame': 7, 'eggs': 7}

isolated = list()
for p in products:
    bizarre = set()
    for i in p.ingredients:
        if i not in safe_ingredients:
            bizarre.add(i)
    if len(bizarre) > 1 and len(p.allergens) > 1:
        # print("* {} contains {}".format(bizarre, p.allergens))
        np = Product()
        np.ingredients = bizarre
        np.allergens = p.allergens
        isolated.append(np)

for a in all_allergens.keys():
    selection = list()
    for p in products:  # isolated
        if a in p.allergens:
            selection.append(p)
    possible = selection[0].ingredients
    for idx in range(1, len(selection)):
        possible = intersection(possible, selection[idx].ingredients)
    print("AA {} => {}".format(a, possible))


# AA peanuts => ['gnrpml', 'xrmxxvn', 'qxfzc']
# AA nuts => ['gnrpml']
# AA dairy => ['gnrpml', 'vmhqr', 'rdfr']
# AA eggs => ['qxfzc', 'rdfr']
# AA wheat => ['gnrpml', 'jxh']
# AA sesame => ['rfmvh', 'qxfzc', 'rdfr']
# AA fish => ['gnrpml', 'rfmvh', 'khpdjv', 'qxfzc']
# AA soy => ['gnrpml', 'khpdjv', 'rdfr']


# AA dairy => ['vmhqr', ]
# AA eggs => ['qxfzc', ]
# AA fish => [, 'khpdjv'']
# AA nuts => ['gnrpml']
# AA peanuts => [ 'xrmxxvn', ]
# AA sesame => ['rfmvh',, ]
# AA soy => ['rdfr']
# AA wheat => ['jxh']

# vmhqr,qxfzc,khpdjv,gnrpml,xrmxxvn,rfmvh,rdfr,jxh



end = time.time()
print("")
print("Done! in {:.3f} ms ".format((end - start)*1000))