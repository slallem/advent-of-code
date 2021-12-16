
# 2021 Day 16 part 2

from functools import reduce
import operator

f = open('input_ex.txt', 'r')
f = open('input.txt', 'r')
lines = f.readlines()

seq = lines[0].strip()
print(seq)

# D2FE28
# 1101 0010 1111 1110 0010 1000
# 110 100 1:0111 1:1110 0:0101 000
# VVV TTT A:AAAA B:BBBB C:CCCC
# 6   4     7      E      5
# 7E5 = 011111100101 binary = 2021 decimal

# Type 4 = literal, other = operator

#print("ABCDEFG"[3:6])

def hextobin(s):
    r = ""
    for c in list(s):
        scale = 16 ## equals to hexadecimal
        num_of_bits = 4
        r += bin(int(c, scale))[2:].zfill(num_of_bits)
    return r


def bintohex(s):
    hexstr = '%0*X' % ((len(s) + 3) // 4, int(s, 2))
    return hexstr


def hextodec(s):
    return int(s, 16)


def cut(s, qty):
    tete = s[0:qty]
    reste = s[qty:]
    return tete, reste


def decode(s, maxiter = -1):
    global versions
    #print("decoding packet {}".format(s))
    sver, s = cut(s, 3)
    #print("sver {}".format(sver))
    iver = hextodec(bintohex(sver))
    versions.append(iver)
    styp, s = cut(s, 3)
    ityp = hextodec(bintohex(styp))
    res = 0
    if ityp == 4:
        # Literal
        print("Packet LITERAL version {} type {} ({},{})".format(iver, ityp, sver, styp))
        litstr = ""
        while True:
            flag, s = cut(s, 1)
            sval, s = cut(s, 4)
            litcar = bintohex(sval)
            litstr += litcar
            #print("flag {} literal {}".format(flag, litcar))
            if flag == '0':
                break
        # calculate result from literal
        res = hextodec(litstr)
        print("Literal value {} = {}".format(litstr, res))
    else:
        # Operator
        print("Packet OPERATOR version {} type {} ({},{})".format(iver, ityp, sver, styp))
        slentypid, s = cut(s, 1)
        values = []
        if slentypid == '0':
            bitstoread = 15
            slen, s = cut(s, bitstoread)
            ilen = hextodec(bintohex(slen))
            print("Packet OPERATOR flag={} reads 15 bits, got length {}".format(slentypid, ilen))
            subpacketsdata, s = cut(s, ilen)
            while len(subpacketsdata) > 0:
                value, subpacketsdata = decode(subpacketsdata)
                values.append(value)
        else:
            bitstoread = 11
            slen, s = cut(s, bitstoread)
            nbpackets = hextodec(bintohex(slen))
            print("Packet OPERATOR flag={} reads 11, nb of packets={}".format(slentypid, nbpackets))
            for i in range(0, nbpackets):
                value, s = decode(s)
                values.append(value)
        # calculate result from type and values
        # Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets.
        # If they only have a single sub-packet, their value is the value of the sub-packet.
        if ityp == 0:
            res = sum(values)
        # Packets with type ID 1 are product packets - their value is the result of multiplying together the values
        # of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
        elif ityp == 1:
            res = reduce(operator.mul, values)
        # Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
        elif ityp == 2:
            res = min(values)
        # Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
        elif ityp == 3:
            res = max(values)
        # Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is
        # greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have
        # exactly two sub-packets.
        elif ityp == 5:
            if values[0] > values[1]:
                res = 1
            else:
                res = 0
        # Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less
        # than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two
        # sub-packets.
        elif ityp == 6:
            if values[0] < values[1]:
                res = 1
            else:
                res = 0
        # Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal
        # to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly
        # two sub-packets.
        elif ityp == 7:
            if values[0] == values[1]:
                res = 1
            else:
                res = 0
        # Other unexpected
        else:
            exit(9) # impossible case

    #print("reste {}".format(s))
    return res, s


# ---- Main

versions = []

binseq = hextobin(seq)
#print(binseq)


result, dummy = decode(binseq)
print()

# Part ONE
print("Part One: {}".format(sum(versions)))

# Part TWO
print("Part Two: {}".format(result))
