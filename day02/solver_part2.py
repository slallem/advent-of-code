
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
nbInvalid2 = 0


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
        # RULE 1
        if nbl < int(times[0]) or nbl > int(times[1]):
            # invalid password
            nbInvalid += 1
        # RULE 2
        letters = list(password)
        let1 = letters[int(times[0])-1]
        let2 = letters[int(times[1])-1]
        nbMatch = 1 if let1 == letter else 0
        nbMatch += 1 if let2 == letter else 0
        if nbMatch != 1:
            # invalid password
            nbInvalid2 += 1

print("RULE1 total: {}, valid: {}, invalid:{}".format(nbPass, nbPass-nbInvalid, nbInvalid))
print("RULE2 total: {}, valid: {}, invalid:{}".format(nbPass, nbPass-nbInvalid2, nbInvalid2))

# 9h21