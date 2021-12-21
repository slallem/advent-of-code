
# 2021 Day 21 part 1

#Player 1 starting position: 2
#Player 2 starting position: 8
pos = [2, 8]

# Example
#pos = [4, 8]

scores = [0, 0]
upto = 1  # Player 1 starts

boardsize = 10  # 1 to 10
maxdice = 100  # sides
dice = 1  # start
rolls = 0
maxscore = 1000


def roll_dice(times):
    global dice
    global rolls
    score = 0
    for i in range(0, times):
        score += dice
        dice = (dice % 100) + 1
        rolls += 1
    return score


while True:
    upto = (upto + 1) % 2
    throw = roll_dice(3)
    pos[upto] = ((pos[upto] - 1 + throw) % boardsize) + 1
    scores[upto] += pos[upto]  # player score increases by its new position
    if scores[upto] >= maxscore:
        break  # we have a winner

print("Dice rolled {} times, winner is P{}, scores are {}".format(rolls, upto + 1, scores))
print("Part #1 result is {}".format(rolls * scores[(upto + 1) % 2]))
