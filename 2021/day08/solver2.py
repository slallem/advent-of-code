
# 2021 Day 8 part 2

f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()


def sort_chars(s):
    ca = list(s)
    ca.sort()
    res = ""
    for x in ca:
        res += x
    return res


def similar(a, b):
    # test how many chars in b exists in a
    ca = list(a)
    cb = list(b)
    occ = 0
    for c in cb:
        if c in ca:
            occ += 1
    return occ


def contains_all_chars(a, b):
    # test if all chars in b exists in a
    return similar(a, b) == len(b)


def decode_ligne(wirings, digits):
    #print("{} {}".format(wirings, digits))
    repl = dict()
    # Find obvious ones
    for w in wirings.copy():
        if len(w) == 2:
            repl[1] = w
            wirings.remove(w)
        elif len(w) == 3:
            repl[7] = w
            wirings.remove(w)
        elif len(w) == 4:
            repl[4] = w
            wirings.remove(w)
        elif len(w) == 7:
            repl[8] = w
            wirings.remove(w)
    # Find 9 (the only one that contains a "4")
    for w in wirings:
        if contains_all_chars(w, repl[4]):
            repl[9] = w
            wirings.remove(w)
            break
    # Find similarities of remaining digits with other already known (1,4,7,8,9)
    for w in wirings.copy():
        sim = "{}{}{}{}{}".format(
            similar(w, repl[1]),
            similar(w, repl[4]),
            similar(w, repl[7]),
            similar(w, repl[8]),
            similar(w, repl[9]),
        )
        print("{} sim {}".format(w, sim))
        # Similarity fingerprints have been found with given single-line example
        if sim == '13255':
            repl[5] = w
            wirings.remove(w)
        elif sim == '12254':
            repl[2] = w
            wirings.remove(w)
        elif sim == '13265':
            repl[6] = w
            wirings.remove(w)
        elif sim == '23355':
            repl[3] = w
            wirings.remove(w)
        elif sim == '23365':
            repl[0] = w
            wirings.remove(w)
    # Here all is known
    # reverse dict
    drep = {v: k for k, v in repl.items()}
    print("{} {}".format(wirings, digits))
    print("{}".format(repl))
    print("{}".format(drep))
    res = ""
    for d in digits:
        res = res + str(drep[d])
    return int(res)


sum = 0
for line in lines:
    values = line.strip().split(",")
    for value in values:
        if len(value) > 0:
            vals = value.split("|")
            wirings = list(map(sort_chars, vals[0].split()))
            odigits = list(map(sort_chars, vals[1].split()))
            res = decode_ligne(wirings, odigits)
            print("found {}".format(res))
            sum += res

print()
print("Total sum is {}".format(sum))
