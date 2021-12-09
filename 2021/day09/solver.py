# 2021 Day 9part 1

f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

carte = dict()
storage_width = 100

# Fill space with values
y = 0
for line in lines:
    if len(line) > 0:
        vals = list(line.strip())
        x = 0
        for val in vals:
            carte[y * 100 + x] = int(val)
            x += 1
        y += 1

nbcols = x
nbrows = y

sum = 0
for y in range(0, nbrows):
    for x in range(0, nbcols):
        value = carte[y * storage_width + x]
        comparisons = []
        if y > 0:
            comparisons.append(carte[(y - 1) * storage_width + x])
        if (y < nbrows-1):
            comparisons.append(carte[(y + 1) * storage_width + x])
        if x > 0:
            comparisons.append(carte[y * storage_width + x - 1])
        if x < nbcols-1:
            comparisons.append(carte[y * storage_width + x + 1])
        nblower = 0
        for comp in comparisons:
            if value < comp:
                nblower += 1
        if nblower == len(comparisons):
            print("Found {} at pos x:{} y:{}".format(value, x, y))
            sum += value + 1

print(sum)
