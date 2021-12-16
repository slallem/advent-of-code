
# 2021 Day 16 part 1

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
    if ityp == 4:
        # Literal
        print("Packet LITERAL  version {} type {} ({},{})".format(iver, ityp, sver, styp))
        lit = ""
        while True:
            flag, s = cut(s, 1)
            sval, s = cut(s, 4)
            lit = bintohex(sval)
            print("flag {} literal {}".format(flag, lit))
            if flag == '0':
                break
    else:
        # Operator
        print("Packet OPERATOR version {} type {} ({},{})".format(iver, ityp, sver, styp))
        slentypid, s = cut(s, 1)
        if slentypid == '0':
            bitstoread = 15
            slen, s = cut(s, bitstoread)
            ilen = hextodec(bintohex(slen))
            print("Packet OPERATOR flag={} reads 15 bits, got length {}".format(slentypid, ilen))
            subpacketsdata, s = cut(s, ilen)
            while len(subpacketsdata) > 0:
                subpacketsdata = decode(subpacketsdata)
        else:
            bitstoread = 11
            slen, s = cut(s, bitstoread)
            nbpackets = hextodec(bintohex(slen))
            print("Packet OPERATOR flag={} reads 11, nb of packets={}".format(slentypid, nbpackets))
            for i in range(0, nbpackets):
                s = decode(s)
    #print("reste {}".format(s))
    return s


# ---- Main ----

versions = []

binseq = hextobin(seq)
print(binseq)

decode(binseq)

if len(versions) < 30:
    print(versions)
print(sum(versions))


# Some UTs and debug notes...

#print(bintohex("11100010"))
#print(hextodec("7E5"))

# test = "ABCDEFGHIJKLMNOP"
# h, test = cut(test, 3)
# print(h)
# h, test = cut(test, 4)
# print(h)
# h, test = cut(test, 1)
# print(h)
# print(test)


#10001010 0000000001001010100000000001101010000000000000101111010001111000
#
# 100 010 1 00000000001001010100000000001101010000000000000101111010001111000
# 100 010 1 00000000001 0 01010100000000001101010000000000000101111 010001111000

# 000 100 0110 00111000110100
#620080001611562C8802118E34
#01100010000000001000000000000000000101100001000101010110001011001000100000000010000100011000111000110100

# 000 100 01010 reste 10110001011 ???
# 101 100 01011
# version 0, type 4



