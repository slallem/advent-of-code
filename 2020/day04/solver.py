import re


passeports = []

expected_keys = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
    #"cid",
]


def data_is_valid(key, value):
    valid = True
    if key == "byr":
        valid = len(value)==4 and int(value) in range(1920, 2002+1)
        # if not valid:
        #     print("invalid value {} for key {}".format(value,key))
    elif key == "iyr":
        valid = len(value)==4 and int(value) in range(2010, 2020+1)
        # if not valid:
        #     print("invalid value {} for key {}".format(value,key))
    elif key == "eyr":
        valid = len(value)==4 and int(value) in range(2020, 2030+1)
        # if not valid:
        #     print("invalid value {} for key {}".format(value,key))
    elif key == "hgt":
        if (re.match(r'^[0-9]+(in)$', value)):
            valid = int(value.split("in")[0]) in range(59, 76)
        elif re.match(r'^[0-9]+(cm)$', value):
            valid = int(value.split("cm")[0]) in range(150, 194)
        if not valid:
            print("invalid value {} for key {}".format(value,key))
    elif key == "hcl":
        valid = re.match(r'^\#[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]$', value)
        if not valid:
            print("invalid value {} for key {}".format(value,key))
    elif key == "ecl":
        valid = re.match(r'^(amb)|(blu)|(brn)|(gry)|(grn)|(hzl)|(oth)$', value)
        if not valid:
            print("invalid value {} for key {}".format(value,key))
    elif key == "pid":
        valid = len(value)==9 and re.match(r'^[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$', value)
        if not valid:
            print("invalid value {} for key {}".format(value,key))
    elif key == "cid":
        valid = True
    else:
        valid = False
    return valid

expected_keys_p2 = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
    #"cid",
]


def passport_is_valid(p):
    kk = [k1 for k1 in p.keys()]
    #print("{}, {}".format(len(kk), kk))
    for ek in expected_keys:
        if not (ek in kk):
            return False
    return True


passeports.append(dict())

f = open('input.txt', 'r')
lines = f.readlines()
for line in lines:
    text = line.strip()
    if len(text) == 0:
        # New record
        # print("new")
        passeports.append(dict())
        # print(len(passeports))
        # print("---")
    else:
        # add adata to record
        entries = text.split(" ")
        for entry in entries:
            arr = entry.split(":")
            passeports[-1][arr[0]] = arr[1]
            # print("add {} {} to {}".format(arr[0], arr[1], cpasseport))


nb_valid = 0
for passeport in passeports:
    if passport_is_valid(passeport):
        if passport_is_valid(passeport):
            valid = True
            for k, v in passeport.items():
                if not data_is_valid(k, v):
                    # print("invalid value {} for key {}".format(v,k))
                    valid = False
                    break
            if valid:
                nb_valid += 1

print("valid ones : {}".format(nb_valid))

#
# eyr:1988
# iyr:2015
# ecl:gry
# hgt:153in
# pid:173cm
# hcl:0c6261
# byr:1966
#
#
# # ...

# part 1 6h35
# part 2 7h12...