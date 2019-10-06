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
    print(xor_two_str(s1, s2))

    # Part 2
    f = open("ciphertext.txt", "w")
    count, msg = get_file("random.txt")
    key = os.urandom(count)
    key = key.decode('latin1')
    encrypted_text = xor_two_str(key, msg)
    f.write(encrypted_text)
    reverse = xor_two_str(encrypted_text, key)
    f.close()

    # Part 3a
    f = open("encrypted-cp-logo.bmp", "wb")
    count, msg = get_bmp_file("cp-logo.bmp")
    key_a = os.urandom(count)
    key_a = key_a.decode('latin1')
    preprocessed_a = preprocess_image(msg)
    encrypted_text_a = xor_two_str(key_a, msg)
    final_encrypt_a = replaceHeader(preprocessed_a, encrypted_text_a, f)
    f.close()

    # Part 3b
    f = open("encrypted-mustang.bmp", "wb")
    count, msg = get_bmp_file("mustang.bmp")
    key_b = os.urandom(count)
    key_b = key_b.decode('latin1')
    preprocessed_b = preprocess_image(msg)
    # TODO For running part 4, replace key_b with key_a so both images are encrypted with the same key
    encrypted_text_b = xor_two_str(key_a, msg)
    final_encrypt_b = replaceHeader(preprocessed_b, encrypted_text_b, f)
    f.close()

    # Part 4
    f = open("overlay_image.bmp", "wb")
    encrypt_both = xor_two_str(final_encrypt_a, final_encrypt_b)
    replaceHeader(preprocessed_a, encrypt_both, f)
    f.close()
main()