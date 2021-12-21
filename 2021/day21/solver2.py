
# 2021 Day 21 part 2 (with a little help)

# Player 1 starting position: 2
# Player 2 starting position: 8
pos = [2, 8]

# Example
#pos = [4, 8]

boardsize = 10  # 1 to 10
maxdice = 3  # sides / universes
maxscore = 21

situations = {}


def compte_victoires(pos1, pos2, score1, score2):
    # Conditions de victoire
    if score1 >= maxscore:
        return 1, 0
    elif score2 >= maxscore:
        return 0, 1
    # Situation déjà connue
    elif (pos1, pos2, score1, score2) in situations:
        return situations[(pos1, pos2, score1, score2)]
    # Sinon calculer
    else:
        res = (0, 0)
        for dice1 in range(1, maxdice+1):
            for dice2 in range(1, maxdice+1):
                for dice3 in range(1, maxdice+1):
                    new_pos1 = ((pos1 + dice1 + dice2 + dice3 - 1) % boardsize) + 1
                    new_score1 = score1 + new_pos1
                    p2wins, p1wins = compte_victoires(pos2, new_pos1, score2, new_score1)  # p2 turn
                    res = (res[0] + p1wins, res[1] + p2wins)
        situations[(pos1, pos2, score1, score2)] = res
        return res


soluce = compte_victoires(pos[0], pos[1], 0, 0)

print(soluce)

print("Part #2 result is {}".format(max(soluce)))
