
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
    instruction_pointer = 0
    iterations = 0
    if debug:
        print("START STATE {}".format(arr))
    while True:
        iterations += 1
        base_code = arr[instruction_pointer]
        opcode = base_code % 100
        mode_c = int(base_code / 100) % 10
        mode_b = int(base_code / 1000) % 10
        mode_a = int(base_code / 10000) % 10
        param1 = arr[instruction_pointer + 1] if instruction_pointer+1 < len(arr) else 0
        param2 = arr[instruction_pointer + 2] if instruction_pointer+2 < len(arr) else 0
        param3 = arr[instruction_pointer + 3] if instruction_pointer+3 < len(arr) else 0
        if debug:
            print("{}".format(arr))
            print("base {} op {} A {} B {} C {}".format(base_code, opcode, mode_a, mode_b, mode_c))
        if opcode == 1:
            # Addition
            #print("val1 {} val2 {}".format(val1, val2))
            val1 = param1 if mode_c else arr[param1]
            val2 = param2 if mode_b else arr[param2]
            arr[param3] = val1 + val2
            instruction_pointer += 4
        elif opcode == 2:
            # Multiplication
            val1 = param1 if mode_c else arr[param1]
            val2 = param2 if mode_b else arr[param2]
            #print("val1 {} val2 {}".format(val1, val2))
            arr[param3] = val1 * val2
            instruction_pointer += 4
        elif opcode == 3:
            # Input
            target_address = arr[instruction_pointer+1]
            arr[target_address] = input_value
            print("Input={}".format(arr[target_address]))
            instruction_pointer += 2
        elif opcode == 4:
            # Output
            val1 = param1 if mode_c else arr[param1]
            print("Output={}".format(val1))
            instruction_pointer += 2
        elif opcode == 5:
            # Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer
            # to the value from the second parameter. Otherwise, it does nothing.
            val1 = param1 if mode_c else arr[param1]
            val2 = param2 if mode_b else arr[param2]
            print("jump-if-true val1 {} val2 {}".format(val1, val2))
            if val1 != 0:
                instruction_pointer = val2
            else:
                instruction_pointer += 3
        elif opcode == 6:
            # Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value
            # from the second parameter. Otherwise, it does nothing.
            val1 = param1 if mode_c else arr[param1]
            val2 = param2 if mode_b else arr[param2]
            print("jump-if-false val1 {} val2 {}".format(val1, val2))
            if val1 == 0:
                instruction_pointer = val2
            else:
                instruction_pointer += 3
        elif opcode == 7:
            # Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the
            # position given by the third parameter. Otherwise, it stores 0.
            val1 = param1 if mode_c else arr[param1]
            val2 = param2 if mode_b else arr[param2]
            arr[param3] = 1 if val1 < val2 else 0
            instruction_pointer += 4
        elif opcode == 8:
            # Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position
            # given by the third parameter. Otherwise, it stores 0.
            val1 = param1 if mode_c else arr[param1]
            val2 = param2 if mode_b else arr[param2]
            arr[param3] = 1 if val1 == val2 else 0
            instruction_pointer += 4
        elif opcode == 99:
            break
        else:
            print("unexpected opcode {}".format(opcode))
        if debug:
            print("AFTER {}".format(arr))
            if iterations == debug_max_iter:
                break
    return arr[0]

debug = False
debug_max_iter = 5

# replace position 1 with the value 12 and replace position 2 with the value 2

#
# print()
# for i in range(100):
#     for j in range(100):
#         res = run_code_ex(values, i, j)
#         #print("{} and {} gives {}".format(i, j, res))
#         if res == 19690720:
#             print("{} and {} gives {}".format(i, j, res))


input_value = 5
print()
print("{}".format(run_code(values)))

print()
print("TESTS")
# print("{}".format(run_code_ex(values,12,2)))
# print("{}".format(run_code([1,1,1,4,99,5,6,0,99])))
# print("{}".format(run_code([1002,4,3,4,33])))
input_value = 9
print("{}".format(run_code([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])))


end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))