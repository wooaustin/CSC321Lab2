import os


# XOR two input strings, outputs as a string
def xor_two_str(a, b):
    if len(a) != len(b):
        return "Error, unequal string length"
    xored = []
    for i in range(len(a)):
        xored_value = ord(a[i]) ^ ord(b[i])
        xored.append(xored_value)
    return ''.join(chr(x) for x in xored)

# XOR two input byte sequences, outputs as a string
def xor_two_bytes(a, b):
    print("a:\n",a)
    print("b:\n",b)


# Returns string representation of the input file
def get_file(file):
    f = open(file)
    s = ""
    count = 0
    while True:
        c = f.read(1)
        if not c:
            return count, s
        count += 1
        s += c


# Returns a list of byte characters, representing the image
def get_bmp_file(file):
    f = open(file, 'rb')
    s = []
    count = 0
    while True:
        c = f.read(1)
        if not c:
            return count, s
        s.append(c)
        count += 1


# Get the first 54-bytes for the header
def preprocess_image(msg):
    s = []
    for i in range(54):
        s.append(msg[i])
    return s


# Replaces the first 54 bytes of the encrypted image with the file header saved from preprocess_image
def replaceHeader(preprocess, image, file):
    count = 0
    s = []
    for i in range(len(image)):
        if count < 54:
            file.write(preprocess[i])
            s.append(preprocess[i])
            count += 1
        else:
            file.write(str.encode(image[i]))
            s.append(str.encode(image[i]))
    return s


def main():
    # Part 1
    s1 = "Darlin dont you go"
    s2 = "and cut your hair!"
    #print(xor_two_str(s1, s2))

    # Part 2
    f = open("ciphertext.txt", "w")
    count, msg = get_file("random.txt")
    key = os.urandom(count)
    key = key.decode('latin1')
    encrypted_text = xor_two_str(key, msg)
    f.write(encrypted_text)
    reverse = xor_two_str(encrypted_text, key)
    f.close()

    #part 3
    #first we read in both files as byte arrays
    f_1_name = 'cp-logo.bmp'
    f_2_name = 'mustang.bmp'

    with open(f_1_name,'rb') as f:
        data_f_1 = bytearray(f.read())

    with open(f_2_name,'rb') as f:
        data_f_2 = bytearray(f.read())

    bmp_header = data_f_2[0:54]
    key1 = os.urandom(len(data_f_1)-54)
    key2 = os.urandom(len(data_f_2)-54)
    print(type(key))
    key_ba_1 = bytearray(key1)
    key_ba_2 = bytearray(key2)
    data_f_1 = data_f_1[54:]
    data_f_2 = data_f_2[54:]

    f_1_xord = bytes(a ^ b for (a,b) in zip(data_f_1,key_ba_1))
    f_2_xord = bytes(a ^ b for (a,b) in zip(data_f_2,key_ba_2))

    f_1_head_incl = bmp_header + f_1_xord
    f_2_head_incl = bmp_header + f_2_xord

    f_1_name = f_1_name[:-4] + "_xord.bmp"
    f_2_name = f_2_name[:-4] + "_xord.bmp"

    with open(f_1_name, 'wb') as f:
        f.write(f_1_head_incl)

    with open(f_2_name, 'wb') as f:
        f.write(f_2_head_incl)

    #part 4
    #very similar to 3 - for this part we just use 1 random key
    #                    with the goal of xoring each encrypted file
    f_1_name = 'cp-logo.bmp'
    f_2_name = 'mustang.bmp'

    with open(f_1_name,'rb') as f:
        data_f_1 = bytearray(f.read())

    with open(f_2_name,'rb') as f:
        data_f_2 = bytearray(f.read())

    bmp_header = data_f_2[0:54]
    key = os.urandom(len(data_f_1)-54)
    print(type(key))
    key_ba = bytearray(key)
    data_f_1 = data_f_1[54:]
    data_f_2 = data_f_2[54:]

    f_1_xord = bytes(a ^ b for (a,b) in zip(data_f_1,key_ba))
    f_2_xord = bytes(a ^ b for (a,b) in zip(data_f_2,key_ba))

    f_1_head_incl = bmp_header + f_1_xord
    f_2_head_incl = bmp_header + f_2_xord

    f_1_name = f_1_name[:-4] + "_xord_IV.bmp"
    f_2_name = f_2_name[:-4] + "_xord_IV.bmp"

    with open(f_1_name, 'wb') as f:
        f.write(f_1_head_incl)

    with open(f_2_name, 'wb') as f:
        f.write(f_2_head_incl)

    combo_xor = bytes(a ^ b for (a,b) in zip(f_1_xord,f_2_xord))
    cmb_xor_head_incl = bmp_header + combo_xor

    with open("combo_xor.bmp",'wb') as f:
        f.write(cmb_xor_head_incl)

main()
