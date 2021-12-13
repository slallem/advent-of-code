
# 2021 Day 13 part 2

#f = open('input_ex.txt', 'r')
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


def display():
    uniques = set()
    xes = list()
    yes = list()
    for dot in dots:
        uniques.add("{},{}".format(dot[0], dot[1]))
        xes.append(dot[0])
        yes.append(dot[1])
    maxx = max(xes)+1
    maxy = max(yes)+1
    for y in range(0, maxy + 1):
        l = ""
        for x in range(0, maxx + 1):
            s = "{},{}".format(x, y)
            if s in uniques:
                l += "# "
            else:
                l += "  "
        print(l)
    print()


for fold in folds:
    #display()
    if fold[0] == "x":
        foldx(fold[1])
    else:
        foldy(fold[1])

display()

# puzzle gives KJBKEUBG
