
# 2021 Day 7 part 1

#f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

initpos = []

for line in lines:
    values = line.strip().split(",")
    for value in values:
        initpos.append(int(value))

population = dict()

for value in initpos:
    if value in population:
        population[value] += 1
    else:
        population[value] = 1

print("start is {}".format(population))
mini = min(population.keys())
maxi = max(population.keys())
print("min is {} max is {}".format(mini, maxi))

possibilities = dict()
minfuel = -1
minpos = -1
for moveto in range(mini, maxi+1):
    fuel = 0
    for k in population.keys():
        fuel += population[k] * abs(moveto - k)
    possibilities[moveto] = fuel
    if minfuel < 0 or fuel < minfuel:
        minfuel = fuel
        minpos = moveto

print("possibilities {} ".format(possibilities))
print("min index is {} with fuel {}".format(minpos, minfuel))
