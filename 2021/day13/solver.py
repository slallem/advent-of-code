
# 2021 Day 13 part 1

f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

dots = []
folds = []

for line in lines:
    if len(line) > 0:
        if "," in line:
            vals = line.strip().split(",")
            dots.append([int(vals[0]), int(vals[1])])
        elif "x=" in line:
            vals = line.strip().split("=")
            folds.append(["x", int(vals[1])])
        elif "y=" in line:
            vals = line.strip().split("=")
            folds.append(["y", int(vals[1])])


def foldx(x):
    print("folding X {}".format(x))
    for dot in dots:
        if dot[0] >= x:
            dot[0] = x - (dot[0] - x)


def foldy(y):
    print("folding Y {}".format(y))
    for dot in dots:
        if dot[1] >= y:
            dot[1] = y - (dot[1] - y)

#print(dots)

#for fold in folds:
if folds[0][0] == "x":
    foldx(folds[0][1])
else:
    foldy(folds[0][1])


# Count unique

uniques = set()
for dot in dots:
    uniques.add("{},{}".format(dot[0], dot[1]))

#print(dots)
print(len(uniques))

