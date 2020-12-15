
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
    values = []
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
            numbers = text.split(",")
            for n in numbers:
                values.append(int(n))
    return values



# regex_examples()

start = time.time()

values = get_values("input.txt")
#print("{}".format(values))


def run_code_ex(arr, noun, verb):
    values[1] = noun
    values[2] = verb
    return run_code(arr)


def run_code(input_arr):
    arr = input_arr.copy()
    adr = 0
    iterations = 0
    while True:
        iterations += 1
        base_code = arr[adr]
        opcode = base_code % 100
        mode_c = int(base_code / 100) % 10
        mode_b = int(base_code / 1000) % 10
        mode_a = int(base_code / 10000) % 10
        # print("{}".format(arr))
        # print("base {} op {} A {} B {} C {}".format(base_code, opcode, mode_a, mode_b, mode_c))
        if opcode == 1:
            # Addition
            adr1 = arr[adr + 1]
            adr2 = arr[adr + 2]
            adr3 = arr[adr + 3]
            val1 = adr1 if mode_c else arr[adr1]
            val2 = adr2 if mode_b else arr[adr2]
            #print("val1 {} val2 {}".format(val1, val2))
            arr[adr3] = val1 + val2
            adr += 4
        elif opcode == 2:
            # Multiplication
            adr1 = arr[adr + 1]
            adr2 = arr[adr + 2]
            adr3 = arr[adr + 3]
            val1 = adr1 if mode_c else arr[adr1]
            val2 = adr2 if mode_b else arr[adr2]
            #print("val1 {} val2 {}".format(val1, val2))
            arr[adr3] = val1 * val2
            adr += 4
        elif opcode == 3:
            # Input
            adr1 = arr[adr + 1]
            val1 = adr1 if mode_c else arr[adr1]
            arr[adr1] = 1 # fixed
            print("Input={}".format(arr[adr1]))
            adr += 2
        elif opcode == 4:
            # Output
            adr1 = arr[adr + 1]
            val1 = adr1 if mode_c else arr[adr1]
            print("Output={}".format(val1))
            adr += 2
        elif opcode == 99:
            break
        else:
            print("unexpected opcode {}".format(opcode))
        # if iterations == 2:
        #     break
    return arr[0]


# replace position 1 with the value 12 and replace position 2 with the value 2

#
# print()
# for i in range(100):
#     for j in range(100):
#         res = run_code_ex(values, i, j)
#         #print("{} and {} gives {}".format(i, j, res))
#         if res == 19690720:
#             print("{} and {} gives {}".format(i, j, res))


print()
print("{}".format(run_code(values)))

print("TESTS")
# print("{}".format(run_code_ex(values,12,2)))
# print("{}".format(run_code([1,1,1,4,99,5,6,0,99])))
# print("{}".format(run_code([1002,4,3,4,33])))

end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))