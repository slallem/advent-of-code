# 06h00

import time
import re

def regex_examples():
    sample = 'les années 1950 à 2000 couvrent 50 années de fooooolie'
    print(re.findall(r'([0-9]+)', sample))
    print(re.findall(r'(ANN)', sample, re.IGNORECASE))
    print(re.findall(r'(xyz)', sample))
    print(re.match(r'^(.+95)', sample) is not None)
    print(re.match(r'xyz', sample) is not None)


def decode_seat(text):
    #FBFBFBFRLR
    chars = text
    print(chars)
    row = 0
    row += 64 if chars[0] == 'B' else 0
    row += 32 if chars[1] == 'B' else 0
    row += 16 if chars[2] == 'B' else 0
    row += 8 if chars[3] == 'B' else 0
    row += 4 if chars[4] == 'B' else 0
    row += 2 if chars[5] == 'B' else 0
    row += 1 if chars[6] == 'B' else 0
    col = 0
    col += 4 if chars[7] == 'R' else 0
    col += 2 if chars[8] == 'R' else 0
    col += 1 if chars[9] == 'R' else 0
    seat = (row * 8) + col
    print("row {} col {} seat {}".format(row, col, seat))
    return seat


def do_the_job(filename):
    available = [True for i in range(128*8)]
    max_seat = 0
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
            seat = decode_seat(data)
            available[seat] = False
            if seat > max_seat:
                max_seat = seat

    print("")
    print("PART #1")
    print("number of lines {}, max seat ID is {}".format(nb_lines, max_seat))

    print("")
    print("PART #2")
    for row in range(128):
        for col in range(8):
            if available[row*8+col]:
                if not available[row*8+col-1]:
                    if not available[row*8+col+1]:
                        print("row {} col {} seat {} is available".format(row, col, row*8+col))


start = time.time()
do_the_job('input.txt')

end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))



# 06h25
