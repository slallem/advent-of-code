
values = []
f = open('input.txt', 'r')
lines = f.readlines()

for row in lines:
    if len(row) > 0:
        values.append(int(row))

# print(values)

nbVal = len(values)
for i in range(0, nbVal - 1):
    a = values[i]
    for j in range(i, nbVal - 1):
        b = values[j]
        for k in range(j, nbVal - 1):
            c = values[k]
            if (a+b+c) == 2020:
                print("{} + {} + {} = {}".format(a, b, c, a+b+c))
                print("{} * {} * {} = {}".format(a, b, c, a*b*c))


# print("--")
#
# nbVal = len(values)
# for i in range(0, nbVal - 1):
#     a = values[i]
#     for j in range(i, nbVal - 1):
#         b = values[j]
#         for k in range(j, nbVal - 1):
#             c = values[k]
#             for kk in range(k, nbVal - 1):
#                 d = values[kk]
#                 if (a+b+c+d) == 2020:
#                     print("{} + {} + {} + {} = {}".format(a, b, c, d, a+b+c+d))
#                     print("{} * {} * {} * {} = {}".format(a, b, c, d, a*b*c*d))
#
# print("--fin")
