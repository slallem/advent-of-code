
# 2021 Day 20 part 1 and 2

#f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

# Read Image Enhancement Algorithm (first line)
image_enhancement_algorithm = list(lines[0].strip())  # aka ['.', '#', '#', '.', '.', ...]
del lines[0]

# Read Input Image
input_image = set()
y = -10
for line in lines:
    if len(line.strip()) > 0:
        y += 1
        x = -10
        for c in list(line.strip()):
            x += 1
            if c == '#':
                input_image.add((x, y))


def display(img: set):
    min_y = min(map(lambda v: v[1], img))
    max_y = max(map(lambda v: v[1], img))
    min_x = min(map(lambda v: v[0], img))
    max_x = max(map(lambda v: v[0], img))
    for y in range(min_y, max_y+1):
        s = ""
        for x in range(min_x, max_x+1):
            s += "#" if (x, y) in img else "."
        print(s)
    print(len(img))
    print()


def evaluate_pixel(img: set, universe_color: chr, pixel: tuple):
    bin_str = ""
    for ofy in (-1, 0, 1):
        for ofx in (-1, 0, 1):
            if universe_color == '.':
                bin_str += "1" if (pixel[0] + ofx, pixel[1] + ofy) in img else "0"
            else:
                bin_str += "0" if (pixel[0] + ofx, pixel[1] + ofy) in img else "1"
    index = int(bin_str, 2)
    return image_enhancement_algorithm[index]


def enhance(img: set, universe_color: chr):
    # consider every squares where a lit pixel is involved
    # aka -2 / +2 around every lit pixels
    # Step 1: identify pixels to evaluate
    pixels = set()
    for pixel in img:
        for ofy in (-2, -1, 0, 1, 2):
            for ofx in (-2, -1, 0, 1, 2):
                pixels.add((pixel[0] + ofx, pixel[1] + ofy))
    # Step 2: reevaluate pixels
    res = set()
    new_universe_color = image_enhancement_algorithm[int("000000000",2)] if universe_color == '.' else image_enhancement_algorithm[int("111111111",2)]
    for pixel in pixels:
        if evaluate_pixel(img, universe_color, pixel) != new_universe_color:  # do not store lit values but difference with universe (all lit or all dark)
            res.add(pixel)
    return res, new_universe_color


#display(input_image)
image = input_image
bg_color = '.'
nb = 2
for i in range(0, nb):
    image, bg_color = enhance(image, bg_color)
    #display(image)

print(f"Part #1 : Lit pixels count is {len(image)} after {nb} enhancements")

image = input_image
bg_color = '.'
nb = 50
for i in range(0, nb):
    image, bg_color = enhance(image, bg_color)

print(f"Part #2 : Lit pixels count is {len(image)} after {nb} enhancements")

exit()
