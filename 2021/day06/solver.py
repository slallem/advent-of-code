
# 2021 Day 6 part 1

#f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

initfishes = []

for line in lines:
    values = line.strip().split(",")
    for value in values:
        initfishes.append(int(value))

population = dict()

for value in initfishes:
    if value in population:
        population[value] += 1
    else:
        population[value] = 1

print("start is {}".format(population))

for day in range(0,80):
    newpop = dict()
    for kind in population.keys():
        nb = population[kind]
        if kind == 0:
            if 6 in newpop:
                newpop[6] += nb
            else:
                newpop[6] = nb
            newpop[8] = nb  # new ones created
        else:
            if kind-1 in newpop:
                newpop[kind-1] += population[kind]
            else:
                newpop[kind-1] = population[kind]
    population = newpop
    sum = 0
    for value in population.values():
        sum += value
    #print("day {} is {} total {}".format(day+1, population, sum))
    print("day {} total {}".format(day+1, sum))

