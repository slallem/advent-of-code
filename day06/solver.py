
import time
import re


def regex_examples():
    sample = 'les années 1950 à 2000 couvrent 50 années de fooooolie'
    print(re.findall(r'([0-9]+)', sample))
    print(re.findall(r'(ANN)', sample, re.IGNORECASE))
    print(re.findall(r'(xyz)', sample))
    print(re.match(r'^(.+95)', sample) is not None)
    print(re.match(r'xyz', sample) is not None)


def decode_ligne(data):
    chars = list(data)
    print("data {}".format(chars))


def do_the_job(filename):
    answers = list()
    answers.append(set())
    nbingroup = 0
    nb_lines = 0
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        text = line.strip()
        if len(text) == 0:
            # empty line
            nb_lines += 0
            #new group
            answers.append(set())
            nbingroup = 0
        else:
            # data line
            data = list(text.strip())
            nb_lines += 1
            #decode_ligne(data)
            #new person in group
            nbingroup += 1
            if nbingroup == 1:
                for letter in data:
                    answers[-1].add(letter)
            else:
                for letter in answers[-1].copy():
                    if letter not in data:
                        answers[-1].remove(letter)
    total = 0
    nbgroupes = 0
    for groupe in answers:
        if len(groupe)>0:
            nbgroupes += 1
            total += len(groupe)
    print("number of lines {}".format(nb_lines))
    print("number of groups {}".format(nbgroupes))
    print("total unique common answers {}".format(total))


# regex_examples()

start = time.time()
do_the_job('input.txt')

end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))

# start 6h00
# part1 06h10
# part2 06h19