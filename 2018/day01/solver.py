
# 2021-11-26

values = []
f = open('input.txt', 'r')
lines = f.readlines()

for row in lines:
    values.append(int(row))

# print(values)

f = 0
freqs = set()
nbval = len(values)
while True:
    for i in range(0, nbval):
        print("was {} plus {} gives {}".format(f, values[i], f+values[i]))
        f = f + values[i]
        if f in freqs:
            print("{} existe deja".format(f))
            exit(9)
        freqs.add(f)
