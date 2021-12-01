
import time
import re


def regex_examples():
    sample = 'les années 1950 à 2000 couvrent 50 années de fooooolie'
    print(re.findall(r'([0-9]+)', sample))
    print(re.findall(r'(ANN)', sample, re.IGNORECASE))
    print(re.findall(r'(xyz)', sample))
    print(re.match(r'^(.+95)', sample) is not None)
    print(re.match(r'xyz', sample) is not None)


# bright white bags contain 2 pale olive bags, 2 dotted black bags.
# clear red bags contain 2 bright chartreuse bags, 5 striped magenta bags.
# mirrored chartreuse bags contain 2 vibrant crimson bags, 2 drab blue bags.

all_bags = dict()


def count_contents(bag1color, level=0):
    # tell if bag1 can contain bag2
    if bag1color == "other bags":  # no other == single bag
        return 1 # this bag
    if bag1color not in all_bags.keys():
        print("***error {}".format(bag1color))
        exit(99)
    bag: dict = all_bags[bag1color]
    if "total" in bag.keys():
        return bag["total"]
    # calc and save
    tot = 1  # this bag
    content: dict = bag["content"]
    for b in content:
        color = b["color"]
        nb = b["nb"]
        tot += count_contents(color, level+1) * nb
    bag["total"] = tot
    all_bags[bag1color] = bag  # save calc
    return tot


# def can_contain_color_bag(bag1color, bag2color):
#     # tell if bag1 can contain bag2
#     if bag1color in all_bags.keys():
#         for b in all_bags[bag1color]["content"]:
#             # print("comparing {} with {}".format(b, bag2))
#             if b["color"] == bag2color:
#                 return True
#             elif can_contain_color_bag(b, bag2color):
#                 return True
#     return False


def decode_ligne(data):
    if " contain " not in data:
        print("*** ERROR invalid line {}".format(data))
        exit(99)
    desc = data.split(" contain ")
    main_bag = desc[0].strip().split(" ")
    subs = desc[1].replace(".", "").strip().split(",")
    color1 = main_bag[0] + " " + main_bag[1]
    desc = dict()
    content = list()
    print("{}".format(main_bag))
    for s in subs:
        sub = s.strip().split(" ")
        color2 = sub[1] + " " + sub[2]
        subb = dict()
        subb["nb"] = int(sub[0].replace("no","0"))
        subb["color"] = color2
        content.append(subb)
    desc["content"] = content
    print("  - {}".format(desc))
    all_bags[color1] = desc


def do_the_job(filename):
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
            decode_ligne(data)
    print("number of lines {}".format(nb_lines))
    search = "shiny gold"
    # counter_1 = 0
    # for bag in all_bags:
    #     if can_contain_color_bag(bag, search):
    #         print("{} can contain {}".format(bag, search))
    #         counter_1 += 1
    # print("possible bags coloour {}".format(counter_1))

    total = count_contents(search)
    print("total bags for {} = {}".format(search, total-1)) # -1 = exclude shiny bag itself




# regex_examples()

start = time.time()
do_the_job('input.txt')

end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))


#doh 7h30... (1h30 to solve 2 stars :(