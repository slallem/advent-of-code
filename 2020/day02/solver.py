
# 2002-12-02 09:00

policies = []
f = open('input.txt', 'r')
lines = f.readlines()


def count_letter(a_text, a_letter):
    counter = 0
    for c in list(a_text):
        if c == a_letter:
            counter += 1
    return counter


nbPass = 0
nbInvalid = 0


for row in lines:
    if len(row) > 0:
        nbPass += 1
        values = row.split(' ')
        times = values[0].split('-')
        letter = values[1].split(':')[0]
        password = values[2]
        # policies.append({"times": times, "letter": letter, "password": password})
        nbl = count_letter(password, letter)
        # print("min [{}] max [{}] letter [{}] password [{}] count [{}]".format())
        if nbl < int(times[0]) or nbl > int(times[1]):
            # invalid password
            nbInvalid += 1

print("total: {}, valid: {}, invalid:{}".format(nbPass, nbPass-nbInvalid, nbInvalid))

# for policy in policies:
#     nbl = count_letter(policy.)
#     if counter()

# print(values)

# nbval = len(values)
# for i in range(0, nbval-1):
#     for j in range(i, nbval):
#         a = values[i]
#         b = values[j]
#         if (a+b) == 2020:
#             print("{} + {} = {}".format(a, b, a+b))
#             print("{} * {} = {}".format(a, b, a*b))
