
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
    decoded = 0
    chars = list(data)
    last = chars[-1]
    cumul = 0
    offset = len(data)/2
    for i in range(len(chars)):
        c = chars[i]
        char_ahead = chars[int((i + offset) % len(data))]
        if c == char_ahead:
            decoded += int(c)
        # if c == last:  # same char
        #     cumul += 1
        # else:  # char change
        #     if cumul > 0:
        #         decoded += int(last) * cumul
        #     cumul = 0
        # last = c
    print("data {}".format(decoded))
    return decoded


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


# regex_examples()

start = time.time()
do_the_job('input.txt')

end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))