
# 2021 Day 2 part 2

f = open('input.txt', 'r')
lines = f.readlines()

aim = 0
horiz = 0
depth = 0

for row in lines:
    words = row.split()
    cmd = words[0]
    value = int(words[1])
    if cmd == 'down':
        aim += value
    elif cmd == 'up':
        aim -= value
    elif cmd == 'forward':
        horiz += value
        depth += (aim * value)

print("aim {} horiz {} depth {} final {}".format(aim, horiz, depth, horiz * depth))
