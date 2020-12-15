
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
            decode_ligne(data)
    print("number of lines {}".format(nb_lines))


def analyze_file(filename):
    nb_numeric = 0
    nb_empty_lines = 0
    nb_lines = 0
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        text = line.strip()
        if len(text) == 0:
            # empty line
            nb_empty_lines += 1
        else:
            # data line
            data = text
            nb_lines += 1
            # decode_ligne(data)
            print(list(data))
            if re.match(r'\d+', data):
                nb_numeric += 1

    print("lines {} non-empty {} empty {}".format(len(lines), nb_lines, nb_empty_lines))
    print("numeric {} non-numeric {}".format(nb_numeric, len(lines) - nb_numeric))


# start = time.time()

# regex_examples()
analyze_file('examples/input-2020-01.txt')

# end = time.time()
# print("")
# print("Done! in {} seconds ".format(end - start))