
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
    res = data
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
# print(combinations([1, 64, 128], range(1,3)))
# exit(9)
# print(combinations(["X", "Y", "Z"]))

def apply_mask(value: int, txt):
    chars = list(txt)
    chars.reverse()
    res = value
    bit: int = 1  #64 bits
    for idx, c in enumerate(chars):
        if c == "1":
            res = res | bit
        elif c == "0":
            res = res & ~bit
        bit = bit << 1
    return res


def apply_mask2(address: int, value: int, txt, mem: dict):
    chars = list(txt)
    chars.reverse()
    res = address
    bit: int = 1  # 64 bits
    possible_bits = list()
    possible_bits.append(0)
    reset_mask = 0
    for idx, c in enumerate(chars):
        if c == "1":  # force bit
            res = res | bit
        elif c == "0":  # unchanged
            pass
        elif c == "X":  # floating
            possible_bits.append(bit)
            reset_mask = reset_mask | bit
        bit = bit << 1
    #print(combinations(["A", "B", "C"], range(2,3)))
    floating_bits_combis = combinations(possible_bits, range(1, len(possible_bits)))
    for combi in floating_bits_combis:
        new_address = res & ~reset_mask
        for b in combi:
            new_address = new_address | b
        mem[new_address] = value


data = read_file('input.txt')

memory = dict()

mask = ""

for line in data:
    parts = line.split("=")
    cmd = parts[0].strip()
    val = parts[1].strip()
    if cmd == "mask":
        # mask
        mask = val
        print("mask is {}".format(mask))
    else:
        # mem
        rr = cmd[4:]
        adr = int(rr[0:len(rr)-1])
        ival = int(val)
        apply_mask2(adr, ival, mask, memory)
        #memory[adr] = ival
        #print("adr is {} value is {}, apply {} new value {}".format(decadr, ival, mask, memory[adr]))


total = 0
for val in memory.values():
    total += val

print("there is {} values and the total is {}".format(len(memory), total))


print("number of lines {}".format(len(data)))

end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))

# 06h43