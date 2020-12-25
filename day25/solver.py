#!/usr/bin/python3

import time
import re
import itertools


def card_handshakes(subject_number: int, expected: int):
    # The handshake used by the card and the door involves an operation that transforms a subject number.
    # To transform a subject number, start with the value 1. Then, a number of times called the loop size,
    # perform the following steps:
    val = 1
    loop = 1
    while True:
        #Set the value to itself multiplied by the subject number.
        val *= subject_number
        #Set the value to the remainder after dividing the value by 20201227.
        val = val % 20201227

        if val == expected:
            break
        loop += 1
    return loop


def transform(subject_number: int, loops: int):
    val = 1
    for i in range(loops):
        #Set the value to itself multiplied by the subject number.
        val *= subject_number
        #Set the value to the remainder after dividing the value by 20201227.
        val = val % 20201227
    return val





start = time.time()

# regex_examples()
# print(combinations(["A", "B", "C"], range(2,3)))
# print(combinations(["X", "Y", "Z"]))

#lines = read_file('input.txt')

#print("number of lines {}".format(len(lines)))


card_pub_key = 15113849
door_pub_key = 4206373

#card_pub_key = 5764801
#door_pub_key = 17807724

card_secret_loop = card_handshakes(7, card_pub_key)
door_secret_loop = card_handshakes(7, door_pub_key)

print("card secret loop {}".format(card_secret_loop))
print("door secret loop {}".format(door_secret_loop))

encryption_key = transform(door_pub_key, card_secret_loop)

print("encryption key {}".format(encryption_key))

print("done")

end = time.time()
print("")
print("Done! in {:.3f} ms ".format((end - start)*1000))