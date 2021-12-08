
# 2021 Day 8 part 1

#f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

sum = 0
for line in lines:
    if len(line) > 0:
        vals = line.split("|")
        odigits = vals[1].split()
        for odigit in odigits:
            if len(odigit) in [2, 4, 3, 7]:  # obvious wiring for 1, 4, 7 and 8
                sum += 1

print(sum)
