
# 2021 Day 24 part 1

# Naïve "full scan" implementation
# Functional but impossible to run in a decent time
# (it can take up days (200+), even optimized)

# Second option => Disassemble the code
# (then understand and find a proper resolution - to come)

import time

start = time.time()

f = open('input_ex.txt', 'r')
modelno = "13579246899999"

#f = open('input.txt', 'r')
lines = f.readlines()

#lines = ["inp z", "inp x", "mul z 3", "eql z x"]
#modelno = "26569999999999"

monad_program = []
for line in lines:
    if len(line.strip()) > 0:
        monad_program.append(line.strip().split(" "))


def alu_run(program, model_number):
    model = list(model_number)
    registers = ('w','x','y','z')
    int_from_bool = {True: 1, False: 0}
    alu = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    for cmd in program:
        if cmd[0] == "inp":
            alu[cmd[1]] = int(model.pop(0))
        elif cmd[0] == "mul":
            if cmd[2] in registers:
                alu[cmd[1]] *= alu[cmd[2]]
            else:
                alu[cmd[1]] *= int(cmd[2])
        elif cmd[0] == "div":
            if cmd[2] in registers:
                alu[cmd[1]] //= alu[cmd[2]]
            else:
                alu[cmd[1]] //= int(cmd[2])
        elif cmd[0] == "add":
            if cmd[2] in registers:
                alu[cmd[1]] += alu[cmd[2]]
            else:
                alu[cmd[1]] += int(cmd[2])
        elif cmd[0] == "mod":
            if cmd[2] in registers:
                alu[cmd[1]] %= alu[cmd[2]]
            else:
                alu[cmd[1]] %= int(cmd[2])
        elif cmd[0] == "eql":
            print(cmd)
            print("before ", alu)
            if cmd[2] in registers:
                alu[cmd[1]] = int_from_bool[(alu[cmd[1]] == alu[cmd[2]])]
            else:
                alu[cmd[1]] = int_from_bool[(alu[cmd[1]] == int(cmd[2]))]
            print("after ", alu)
        else:
            print("Error invalid command: " + cmd)
            exit(99)
    return alu


# Example

alu = alu_run(monad_program, modelno)
print(alu)


nb = 0
maxiter = 9*9*9*9*9*9*9*9*9*9*9*9*9*9
for i in range(99999999999999, 11111111111111-1, -1):
    modnum = str(i)
    if '0' not in modnum:
        nb += 1
        #alu = alu_run(monad_program, modnum)
        if nb % 100000 == 0:
            #print("Done! in {:.3f} ms ".format((end - start)*1000))
            elapsed_ms = (time.time() - start)*1000
            ms_per_iter = elapsed_ms / nb
            remaining = (maxiter - nb) * ms_per_iter
            print("Trying {} z {} time per job {:.3f}ms. remaining time {:.3f} (days)".format(modnum, alu['z'], ms_per_iter, remaining // 1000 // 60 // 60 / 24))

        if alu['z'] == 0:
            exit(0)




# then find number from input startiung by 99999999999999 to 11111111111111


print("end")

