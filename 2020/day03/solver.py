
# 2002-12-03 06:00

policies = []

f = open('input.txt', 'r')
terrain = f.readlines()


def slope(xx, yy):
    nbMoves = 0
    nbDots = 0
    nbTrees = 0

    x = 0
    y = 0
    lastLine = len(terrain)-1

    while True:
        y += yy
        lineLength = len(terrain[y])
        if lineLength > 0:
            nbMoves += 1
            x += xx
            chars = list(terrain[y].strip())
            car = chars[(x % len(chars))]
            # print(len(chars), end="")
            # print(car, end="")
            if car == '#':
                nbTrees += 1
            elif car == '.':
                nbDots += 1
            # else:
            # print(">>>{}<<<".format(car))
            if y >= lastLine:
                break

    print("slope for x {} y {} moves {} dots {} trees {} total {}".format(xx, yy, nbMoves, nbDots, nbTrees, nbDots+nbTrees))
    return nbTrees


# slope(1, 1)
# slope(3, 1)
# slope(5, 1)
# slope(7, 1)
# slope(1, 2)

print(slope(1, 1) * slope(3, 1) * slope(5, 1) * slope(7, 1) * slope(1, 2))

# end 6h30
