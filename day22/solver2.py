#!/usr/bin/python3

import time
import re
import itertools
import copy


def regex_examples():
    sample = 'les années 1950 à 2000 couvrent 50 années de fooooolie'
    print(re.findall(r'([0-9]+)', sample))
    print(re.findall(r'(ANN)', sample, re.IGNORECASE))
    print(re.findall(r'(xyz)', sample))
    print(re.match(r'^(.+95)', sample) is not None)
    print(re.match(r'xyz', sample) is not None)
    print(re.match(r'^([ a-z0-9^:]+):.([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)$', "departure date: 41-532 or 552-956").groups())


def combinations(items: list, r: range = None):
    c = list()
    if r is None:
        r = range(1, len(items)+1)
    for i in r:
        c.extend(list(itertools.combinations(items, i)))
    return c


def decode_ligne(data):
    res = list(data)
    #print("data {}".format(chars))
    return res


def read_file(filename):
    res = list()
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
            res.append(decode_ligne(data))
    return res


start = time.time()

# regex_examples()
# print(combinations(["A", "B", "C"], range(2,3)))
# print(combinations(["X", "Y", "Z"]))

# lines = read_file('input.txt')
# print("number of lines {}".format(len(lines)))

def subgame(p1, p2):
    pass






player1 = [10,39,16,32,5,46,47,45,48,26,36,27,24,37,49,25,30,13,23,1,9,3,31,14,4]
player2 = [2,15,29,41,11,21,8,44,38,19,12,20,40,17,22,35,34,42,50,6,33,7,18,28,43]

# player1 = [43,19]
# player2 = [2,29,14]

# player1 = [9, 2, 6, 3, 1]
# player2 = [5, 8, 4, 7, 10]

game_id = 0


def run_game(deck1: list, deck2: list, depth=1, verbose=False):
    global game_id
    game_id += 1
    this_game_id = game_id

    previous_states = list()
    state = format("{}{}".format(deck1, deck2))
    last_state = state

    pli = 0
    while True:
        pli += 1
        if verbose:
            print("--- Game {} Round {} ".format(this_game_id, pli))

        # endless loop protection
        state = format("{}{}".format(deck1, deck2))
        for ps in previous_states:
            if ps == state:
                if verbose:
                    print("Same configuration already encountered")
                return 1, deck1, deck2
        previous_states.append(state)

        if verbose:
            print("Player 1's deck: {}".format(deck1))
            print("Player 2's deck: {}".format(deck2))

        p1 = deck1.pop(0)
        p2 = deck2.pop(0)

        if verbose:
            print("Player 1 plays: {}".format(p1))
            print("Player 2 plays: {}".format(p2))

        if len(deck1) >= p1 and len(deck2) >= p2:
            # Both players have enough cards
            # so, play a sub game !
            if verbose:
                print("Playing a sub-game to determine the winner...")
                print()
            mini_deck_1 = copy.deepcopy(deck1[:p1])
            mini_deck_2 = copy.deepcopy(deck2[:p2])
            winner, l1, l2 = run_game(mini_deck_1, mini_deck_2, depth+1)
            if verbose:
                print("...anyway, back to game {}.".format(this_game_id))
            if winner == 1:
                # p1 wins
                deck1.append(p1)
                deck1.append(p2)
            else:
                # p2 wins
                deck2.append(p2)
                deck2.append(p1)
        else:
            # not enough cards for a sub game
            # classic game
            if p1 > p2:
                winner = 1
            else:
                winner = 2
            ma = max(p1, p2)
            mi = min(p1, p2)
            if winner == 1:
                # p1 wins
                deck1.append(ma)
                deck1.append(mi)
            else:
                # p2 wins
                deck2.append(ma)
                deck2.append(mi)

        # selon le gagnant...
        if verbose:
            print("Player {} wins round {} of game {} !".format(winner, pli, this_game_id))

        if len(deck1) == 0 or len(deck2) == 0:
            if verbose:
                print("end of game ; one player is running out of card")
            break

    if len(deck1) == 0:
        winner = 2
    else:
        winner = 1
    return winner, deck1, deck2



winner, res1, res2 = run_game(player1, player2)

print("P1 {}".format(player1))
print("P2 {}".format(player2))

# calculate score
score = 0
deck = player1
if len(player1) == 0:
    deck = player2

tot = 0
for i in range(1, len(deck)+1):
    print("{} * {} = {}".format(deck[len(deck)-i], i, deck[len(deck)-i]*i))
    tot += (deck[len(deck)-i] * i)
print("TOTAL SCORE {}".format(tot))


end = time.time()
print("")
print("Done! in {:.3f} ms ".format((end - start)*1000))