#!/usr/bin/env python

import time
import re
import itertools
import signal

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


# jmp +301
# acc +27
# nop +299
# jmp +168

def decode_ligne(data):
    #chars = list(data)
    #print("data {}".format(chars))
    ops = data.split(" ")
    cmd = dict()
    cmd["op"] = ops[0]
    v = ops[1]
    if "+" in v:
        cmd["p1"] = int(ops[1][1:])
    else:
        cmd["p1"] = int(ops[1])
    #print("{} {} ".format(ops, cmd))
    return cmd


def lire_fichier(filename):
    prog = list()
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
            prog.append(decode_ligne(data))
    #print("number of lines {}".format(nb_lines))
    return prog


def run_prog(prog: list, start_acc=0, start_adr=0, timeout=2, verbose=True):
    already_exec = set()
    acc = start_acc
    iptr: int = start_adr
    t_start = time.time()
    while True:
        if verbose:
            print("{:0>8d} ".format(iptr), end="")
        t_end = time.time()
        if (t_end - t_start) > timeout:
            raise Exception("** Time {} is over timeout {}, exits".format(t_end - t_start, timeout))
        if iptr in already_exec:
            if verbose:
                print("line {} already executed once".format(iptr))
            break
        already_exec.add(iptr)
        cmd = prog[iptr]
        op = cmd["op"]
        p1 = cmd["p1"]
        if verbose:
            print("{:5} {:5} ".format(op, p1), end="")
        if op == "jmp":
            # relative jump
            if verbose:
                print("jmp relative {} to {} ".format(p1, iptr))
            iptr += p1
        elif op == "nop":
            #do nothing
            if verbose:
                print("nop ".format())
            iptr += 1
        elif op == "acc":
            #no nothing
            if verbose:
                print("acc set value relative {} now is {} ".format(p1, acc))
            acc += p1
            iptr += 1
        elif op == "acc":
            raise Exception("*** unknown instruction {} {} ".format(op, p1))
            exit(99)
        if iptr >= len(prog):
            print("program ended normally")
            break  # end reached
    return acc


start = time.time()

# regex_examples()
# print(combinations(["A", "B", "C"], range(2,3)))
# print(combinations(["X", "Y", "Z"]))

program = lire_fichier('input.txt')

for i in range(len(program)):
    if program[i]["op"] == "jmp":
        print("There is a jmp at {} ... ".format(i), end="")

        # full copy
        prg = list()
        for cmd in program:
            prg.append(cmd.copy())

        prg[i]["op"] = "nop"
        try:
            print(run_prog(prog=prg, start_acc=0, start_adr=0, timeout=1, verbose=False))
        except:
            print("error occured")


#print(run_prog(prog=program, start_acc=0, start_adr=0, timeout=10))

end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))

# 6h46
# part1 00:23:50
# part2 00:46:17

