
import time
import re


def regex_examples():
    sample = 'les années 1950 à 2000 couvrent 50 années de fooooolie'
    print(re.findall(r'([0-9]+)', sample))
    print(re.findall(r'(ANN)', sample, re.IGNORECASE))
    print(re.findall(r'(xyz)', sample))
    print(re.match(r'^(.+95)', sample) is not None)
    print(re.match(r'xyz', sample) is not None)


def decode_ligne(data):
    chars = list(data)
    print("data {}".format(chars))


def get_values(filename):
    res = []
    nb_lines = 0
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        text = line.strip()
        if len(text) == 0:
            # empty line
            nb_lines += 0
        else:
            # data line
            nb_lines += 1
            data = text.strip()
            res.append(int(data))
    return res


start = time.time()

values = get_values("input.txt")
print("{}".format(values))

def get_fuel_from_mass(mass):
    fuel = int(mass/3)-2
    return fuel if fuel > 0 else 0

def get_fuel_total(mass):
    cmass = mass
    fueltotal = 0
    while True:
        fuel = get_fuel_from_mass(cmass)
        if fuel > 0:
            fueltotal += fuel
            cmass = fuel
        else:
            break
    return fueltotal

sum = 0
for mm in values:
    sum += get_fuel_total(mm)



print(get_fuel_from_mass(12))
print(get_fuel_from_mass(14))
print(get_fuel_from_mass(1969))
print(get_fuel_from_mass(100756))

# print(int(12/3)-2)
# print(int(14/3)-2)
# print(int(1969/3)-2)
# print(int(100756/3)-2)
print()

print(sum)

end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))