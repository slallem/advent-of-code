
import time
import re
import json


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

class Bag:
    total: int
    color: str
    qty: int
    contents = list()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

all_bags = dict()


def count_contents(bag1color):
    # tell if bag1 can contain bag2
    if bag1color not in all_bags.keys():
        print("***error {}".format(bag1color))
        exit(99)
    bag: Bag = all_bags[bag1color]
    if bag.total >= 0:  # -1 mean "not yet determined"
        return bag.total
    # calc and save
    bag.total = 1  # this bag
    for b in bag.contents:
        bag.total += count_contents(b.color) * b.qty
    #all_bags[bag1color] = bag  # save calc
    return bag.total


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
    bag = Bag()
    bag.total = -1
    for s in subs:
        sub_bag = Bag()
        sub_bag.total = -1
        m = re.match(r".*(\d+|no) (.+) bag", s)

        # print(s)
        # print(m.groups())
        # print(m.groups()[0])

        # sub = s.strip().split(" ")
        # color2 = sub[1] + " " + sub[2]
        # sub_bag.qty = int(sub[0].replace("no","0"))
        # sub_bag.color = color2

        sub_bag.qty = int(m.groups()[0].replace("no", "0"))
        sub_bag.color = m.groups()[1]
        if sub_bag.qty > 0:
            bag.contents.append(sub_bag)
    all_bags[color1] = bag


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
do_the_job('input2.txt')

end = time.time()
print("")
print("Done! in {} seconds ".format(end - start))


#doh 7h30... (1h30 to solve 2 stars :(