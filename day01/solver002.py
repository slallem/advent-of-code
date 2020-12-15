
values = []
f = open('input.txt', 'r')
lines = f.readlines()

for row in lines:
    if len(row) > 0:
        values.append(int(row))

# print(values)

nbVal = len(values)
for i in range(0, nbVal - 1):
    for j in range(i, nbVal - 1):
        for k in range(0, nbVal):
            if k != i and k != j:
                a = values[i]
                b = values[j]
                c = values[k]
                if (a+b+c) == 2020:
                    print("{} + {} + {} = {}".format(a, b, c, a+b+c))
                    print("{} * {} * {} = {}".format(a, b, c, a*b*c))

# 2002-12-01 12h16