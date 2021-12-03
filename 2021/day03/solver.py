
# 2021 Day 3 part 1

f = open('input.txt', 'r')
lines = f.readlines()

gamma = 0
epsilon = 0
for i in range(0, 12):
    mask = 1 << i
    print("mask {}".format(mask))
    zeroes = 0
    ones = 0
    for row in lines:
        value = int(row, 2)
        if value & mask == 0:
            zeroes += 1
        else:
            ones += 1
    if ones > zeroes:
        gamma += mask
    else:
        epsilon += mask

print("gamma {} epsilon {} soluce {}".format(gamma, epsilon, gamma * epsilon))
