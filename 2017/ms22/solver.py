
import time
import re


def regex_examples():
    sample = 'les années 1950 à 2000 couvrent 50 années de fooooolie'
    print(re.findall(r'([0-9]+)', sample))
    print(re.findall(r'(ANN)', sample, re.IGNORECASE))
    print(re.findall(r'(xyz)', sample))
    print(re.match(r'^(.+95)', sample) is not None)
    print(re.match(r'xyz', sample) is not None)

# Array of String [ ['hello'], ['world'] ]
def read_file_lines(file, ignore_empty=True):
    res = []
    f = open(file, 'r')
    lines = f.readlines()
    for line in lines:
        text = line.strip()
        if (not ignore_empty) or (len(text) > 0):
            res.append(text)
    return res

# Array of Array of Char [ ['h','e','l','l','o'], ['w','o','r','l','d'] ]
def read_file_chars(file, ignore_empty=True):
    res = []
    lines = read_file_lines(file, ignore_empty)
    for line in lines:
        res.append(list(line))
    return res


def decode_ligne(data):
    chars = list(data)
    print("data {}".format(chars))


def do_the_job(filename):
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
            data = text.strip()
            nb_lines += 1
            decode_ligne(data)
    print("number of lines {}".format(nb_lines))


grid = set()

def is_infected(x, y):
    position = "r{}c{}".format(y, x)
    return position in grid

def set_infected(x, y, value):
    position = "r{}c{}".format(y, x)
    if value:
        grid.add(position)
    else:
        grid.remove(position)


# regex_examples()

start = time.time()
#do_the_job('input.txt')

# Read as array of rows, then columns
lines = read_file_chars('input.txt')

already_infected = 0
for j in range(len(lines)):
    for i in range(len(lines[j])):
        if lines[j][i] == '#':
            set_infected(i, j, True)
            already_infected += 1

print(grid)

iterations = 0
infected = 0
cleaned = 0

# virus carrier
px = int(len(lines[0])/2)
py = int(len(lines)/2)
# face up (move delta x/y)
direction = "U"

for repeat in range(10000):
    #burst
    iterations += 1

    current_spot_infected = is_infected(px, py)

    # STEP 1 rotation
    if current_spot_infected:
        # Turn RIGHT
        if direction == "U":
            direction = "R"
        elif direction == "D":
            direction = "L"
        elif direction == "L":
            direction = "U"
        else:  #"R"
            direction = "D"
    else:  # Clean
        # Turn LEFT
        if direction == "U":
            direction = "L"
        elif direction == "D":
            direction = "R"
        elif direction == "L":
            direction = "D"
        else:  #"R"
            direction = "U"

    # Step 2 infection
    if current_spot_infected:  # infected
        set_infected(px, py, False)  # clean it
        if py in range(len(lines)) and px in range(len(lines[0])):
            lines[py][px] = "."
        cleaned += 1
    else:  # clean
        set_infected(px, py, True) # infect it
        if py in range(len(lines)) and px in range(len(lines[0])):
            lines[py][px] = "#"
        infected += 1
    # move forward
    if direction == "U":
        py -= 1
    elif direction == "D":
        py += 1
    elif direction == "L":
        px -= 1
    else:  #"R"
        px += 1


print("px {} py {}".format(px, py))
print("grid entries {}".format(len(grid)))

print("")
for j in range(len(lines)):
    for i in range(len(lines[j])):
        if px == i and py ==j:
            print("[{}]".format(lines[j][i]), end="")
        else:
            print(" {} ".format(lines[j][i]), end="")
    print()
print("")

print("initially infected {} iterations {} infected {} cleaned {}".format(already_infected, iterations, infected, cleaned))


end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))