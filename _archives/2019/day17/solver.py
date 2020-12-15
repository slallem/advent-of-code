
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


def get_param_value(mem, param, mode, relative):
    if mode == 1:
        # Immediate mode
        return param
    elif mode == 0:
        # Position mode
        return read_memory(mem, param)
    elif mode == 2:
        # Relative mode
        return read_memory(mem, relative + param)

def set_mem_value(mem, param, mode, relative, val):
    if mode == 1:
        # Immediate mode = ERROR
        pass
    elif mode == 0:
        # Position mode
        write_memory(mem, param, val)
    elif mode == 2:
        # Relative mode
        write_memory(mem, relative + param, val)


def run_code(mem):
    global input_value_counter
    instruction_pointer = 0
    relative_base = 0
    iterations = 0
    while True:
        iterations += 1
        base_code = read_memory(mem, instruction_pointer)
        opcode = base_code % 100
        mode_c = int(base_code / 100) % 10
        mode_b = int(base_code / 1000) % 10
        mode_a = int(base_code / 10000) % 10
        param1 = read_memory(mem, instruction_pointer+1)
        param2 = read_memory(mem, instruction_pointer+2)
        param3 = read_memory(mem, instruction_pointer+3)
        #print("IPtr {} Code {}: Op.{} M1:{} M2:{} M3:{}".format(instruction_pointer, base_code, opcode, mode_c, mode_b, mode_a))
        if debug:
            print("{:0>8d} {:0>5d} ... ".format(instruction_pointer, base_code, opcode, mode_c, mode_b, mode_a), end="")
        if opcode == 1:
            # Addition
            # print("val1 {} val2 {}".format(val1, val2))
            val1 = get_param_value(mem, param1, mode_c, relative_base)
            val2 = get_param_value(mem, param2, mode_b, relative_base)
            set_mem_value(mem, param3, mode_a, relative_base, val1 + val2)
            if debug:
                print("Addition {} + {} = {} dans {}".format(val1, val2, val1+val2, param3))
            instruction_pointer += 4
        elif opcode == 2:
            # Multiplication
            val1 = get_param_value(mem, param1, mode_c, relative_base)
            val2 = get_param_value(mem, param2, mode_b, relative_base)
            set_mem_value(mem, param3, mode_a, relative_base, val1 * val2)
            if debug:
                print("Multiplication {} * {} = {} dans {}".format(val1, val2, val1*val2, param3))
            instruction_pointer += 4
        elif opcode == 3:
            # Input
            #val1 = get_param_value(mem, param1, mode_c, relative_base)
            val = ord(input_value[input_value_counter])
            #global input_value_counter
            input_value_counter = (input_value_counter + 1) % len(input_value)
            set_mem_value(mem, param1, mode_c, relative_base, val)
            if debug:
                print("Input={}".format(val))
            print("Input={}".format(val))
            instruction_pointer += 2
        elif opcode == 4:
            # Output
            val1 = get_param_value(mem, param1, mode_c, relative_base)
            if debug:
                print("Output={}".format(val1))
            else:
                if val1 > 128:
                    print("[NON-ASCII:{}]".format(val1), end="")
                else:
                    print("{}".format(chr(val1)), end="")
            instruction_pointer += 2
        elif opcode == 5:
            # Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer
            # to the value from the second parameter. Otherwise, it does nothing.
            val1 = get_param_value(mem, param1, mode_c, relative_base)
            val2 = get_param_value(mem, param2, mode_b, relative_base)
            if debug:
                print("Jump-if-true val1 {} val2 {} ==> ".format(val1, val2), end="")
            if val1 != 0:
                instruction_pointer = val2
                if debug:
                    print("Jump to {}".format(val2))
            else:
                instruction_pointer += 3
                if debug:
                    print("No Jump")
        elif opcode == 6:
            # Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value
            # from the second parameter. Otherwise, it does nothing.
            val1 = get_param_value(mem, param1, mode_c, relative_base)
            val2 = get_param_value(mem, param2, mode_b, relative_base)
            if debug:
                print("Jump-if-false val1 {} val2 {} ==> ".format(val1, val2), end="")
            if val1 == 0:
                instruction_pointer = val2
                if debug:
                    print("Jump to {}".format(val2))
            else:
                instruction_pointer += 3
                if debug:
                    print("No Jump")
        elif opcode == 7:
            # Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the
            # position given by the third parameter. Otherwise, it stores 0.
            val1 = get_param_value(mem, param1, mode_c, relative_base)
            val2 = get_param_value(mem, param2, mode_b, relative_base)
            val = 1 if val1 < val2 else 0
            set_mem_value(mem, param3, mode_a, relative_base, val)
            if debug:
                print("Less-Than : {} < {} = {} stored in {}".format(val1, val2, val, param3))
            instruction_pointer += 4
        elif opcode == 8:
            # Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position
            # given by the third parameter. Otherwise, it stores 0.
            val1 = get_param_value(mem, param1, mode_c, relative_base)
            val2 = get_param_value(mem, param2, mode_b, relative_base)
            val = 1 if val1 == val2 else 0
            set_mem_value(mem, param3, mode_a, relative_base, val)
            if debug:
                print("Equals : {} < {} = {} stored in {}".format(val1, val2, val, param3))
            instruction_pointer += 4
        elif opcode == 9:
            # Opcode 9 adjusts the relative base by the value of its only parameter.
            # The relative base increases (or decreases, if the value is negative) by the value of the parameter.
            val1 = get_param_value(mem, param1, mode_c, relative_base)
            relative_base += val1
            if debug:
                print("Adjusts relative_base by {} ; base is now {}".format(val1, relative_base))
            instruction_pointer += 2
        elif opcode == 99:
            print("EXIT PROGRAM")
            break
        else:
            print("unexpected opcode {}".format(opcode))
        # if iterations > 100:
        #     break
    return read_memory(mem, 0)


debug = False

# replace position 1 with the value 12 and replace position 2 with the value 2

#
# print()
# for i in range(100):
#     for j in range(100):
#         res = run_code_ex(values, i, j)
#         #print("{} and {} gives {}".format(i, j, res))
#         if res == 19690720:
#             print("{} and {} gives {}".format(i, j, res))


def init_memory(arr):
    mem = dict()
    for i in range(len(arr)):
        mem[i] = arr[i]
    return mem


def read_memory(mem, adr):
    if adr in mem.keys():
        return mem[adr]
    else:
        return 0


def write_memory(mem, adr, val):
    if val != 0:
        mem[adr] = val
    else:
        if adr in mem.keys():
            del mem[adr]


#TRAINING
#values = [1102,34915192,34915192,7,4,7,99,0]
#values = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]

# values = [4,7,109,7,204,7,99,
#           17,222,333,444,555,666,777,888,999,1010,1111,1212,1313,1414,1515,1616,1717,1818,1919,2020]

# 1102,34463338,34463338,63,1007,63,34463338,63,1005,63
# 53,1101,0,3,1000,109,988,209,12,9,1000,209,6,

input_value_counter = 0
input_value = list(
     "B,A,B,C,A,B,C,A,B,C"+chr(10)
    +"R,8,R,4,L,6,6"+chr(10)
    +"L,6,6,L,6,6,L,6,L,6"+chr(10)
    +"L,6,6,L,6,R,6,6,R,8"+chr(10)
    +"n"+chr(10)
)


# for part 2
#input_value = 2
values[0] = 2
memory = init_memory(values)

print()
print("{}".format(run_code(memory)))

# print()
# print("TESTS")
# print("{}".format(run_code_ex(values,12,2)))
# print("{}".format(run_code([1,1,1,4,99,5,6,0,99])))
# print("{}".format(run_code([1002,4,3,4,33])))
# input_value = 9
# print("{}".format(run_code([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
#  1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
#  999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])))





end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))