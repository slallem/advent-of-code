
# 2002-12-01 11h56

values = []
f = open('input.txt', 'r')
lines = f.readlines()

for row in lines:
    if len(row) > 0:
        values.append(int(row))

# print(values)

nbval = len(values)
for i in range(0, nbval-1):
    for j in range(i, nbval):
        a = values[i]
        b = values[j]
        if (a+b) == 2020:
            print("{} + {} = {}".format(a, b, a+b))
            print("{} * {} = {}".format(a, b, a*b))
