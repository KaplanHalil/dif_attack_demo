import random

sbox1         = [1, 9, 6, 13, 7, 3, 5, 15, 2, 12, 14, 10, 4, 11, 8, 0]
reverse_sbox1 = [15, 0, 8, 5, 12, 6, 2, 4, 14, 1, 11, 13, 9, 3, 10, 7]
# Sbox2'nin tersi kendisine eşit.
sbox2         = [0, 1, 9, 6, 13, 7, 3, 5, 15, 2, 12, 14, 10, 4, 11, 8]
reverse_sbox2 = [0, 1, 9, 6, 13, 7, 3, 5, 15, 2, 12, 14, 10, 4, 11, 8]
# Perm 1 i düzenledim
perm1 = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
perm2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
Mkey = [2, 4, 5, 11]

# Returns array with 4 random integer as a key.
def random_key():
    key = [0]*4
    for i in range(0, 4):
        key[i] = random.randint(0, random.randint(10, 15))

    return key

def cipher1round(girdi, anahtar,sbox,perm):
    # Define empty arrays
    sboxcikti = [0] * 4; permgirdi = [0] * 4
    permara = [0] * 16 ; permcikti = [0] * 4
    keyxorcikti = [0] * 4
    # S-box
    for i in range(0, 4):
        sboxcikti[i] = sbox[girdi[i]]
    # Permutation
    permgirdi = integer_to_bit_array(sboxcikti, 4)
    for i in range(0, 16):
        permara[i] = permgirdi[perm[i]]
    permcikti = bit_array_to_integer(permara, 4)
    # Key xor
    for i in range(0, 4):
        keyxorcikti[i] = permcikti[i] ^ anahtar[i]

    return keyxorcikti


def print_ddt(sbox, inputsize):
    # Defines two-dimensional array for DDT
    ddt_values = [[0 for x in range(pow(2, inputsize))] for y in range(pow(2, inputsize))]
    for dx in range(pow(2, inputsize)):

        for x in range(pow(2, inputsize)):
            # Calculates y and dy according to x and dx
            x1 = dx ^ x
            y = sbox[x]
            y1 = sbox[x1]
            dy = y ^ y1

            # Sets values of the DDT
            ddt_values[dx][dy] = ddt_values[dx][dy] + 1

    for element in ddt_values:
        print(element)


def xor(a, b, size):
    # Define empty array
    c = [0] * size

    for i in range(0, size):
        c[i] = a[i] ^ b[i]
    return c


def integer_to_bit_array(nums, num_bits):
    bit_array = []
    for num in nums:
        binary_representation = bin(num)[2:].zfill(num_bits)  # Convert num to binary string
        bit_array.extend(list(map(int, binary_representation)))  # Append each bit to the bit_array
    return bit_array


def bit_array_to_integer(bits, num_bits):
    return [int(''.join(map(str, bits[i:i + num_bits])), 2) for i in range(0, len(bits), num_bits)]


def keyScheduleFunc(Mkey):
    # Define empty arrays
    key1 = [0] * 16
    key2 = [0] * 16

    key1 = integer_to_bit_array(Mkey, 4)
    for i in range(0, 15):
        key2[i] = key1[i + 1]
    key2[15] = key1[15] ^ key1[13] ^ key1[11] ^ key1[10]
    return bit_array_to_integer(key2, 4)


def keySchedules(Mkey, round):
    # Define empty arrays
    key1 = [0] * 4; key2 = [0] * 4
    key3 = [0] * 4; key4 = [0] * 4
    key5 = [0] * 4; key6 = [0] * 4
    # Computes round keys
    key1 = keyScheduleFunc(Mkey); key2 = keyScheduleFunc(key1)
    key3 = keyScheduleFunc(key2); key4 = keyScheduleFunc(key3)
    key5 = keyScheduleFunc(key4); key6 = keyScheduleFunc(key5)
    #Returns corresponding round key
    if round == 0:
        return Mkey
    elif round == 1:
        return key1
    elif round == 2:
        return key2
    elif round == 3:
        return key3
    elif round == 4:
        return key4
    elif round == 5:
        return key5
    elif round == 6:
        return key6

def s_box_inverse(girdi,sbox):
    cikti = [0]*4

    # S-box
    for i in range(0, 4):
        cikti[i] = sbox[girdi[i]]
    return cikti


def cipher1(girdi, masterkey):
    # Define empty arrays
    round1 = [0] * 4; round2 = [0] * 4
    round3 = [0] * 4; round4 = [0] * 4
    round41 = [0] * 4; cikti = [0] * 4
    key0 = [0] * 4

    # First tree rounds
    key0 = keySchedules(masterkey, 0)
    keywhitening = xor(girdi,key0 ,4)
    round1 = cipher1round(keywhitening,keySchedules(masterkey,1),sbox1,perm1)
    round2 = cipher1round(round1, keySchedules(masterkey, 2),sbox1,perm1)
    round3 = cipher1round(round2, keySchedules(masterkey, 3),sbox1,perm1)
    round4 = xor(round3,keySchedules(masterkey,4),4)
    # Last round S-box
    for i in range(0, 4):
        round41[i] = sbox1[round4[i]]
    cikti = xor(round41,keySchedules(masterkey,5),4)
    return cikti

def cipher2(girdi, masterkey):
    # Define empty arrays
    round1 = [0] * 4; round2 = [0] * 4
    round3 = [0] * 4; round4 = [0] * 4
    round41 = [0] * 4; cikti = [0] * 4
    key0 = [0] * 4

    # First tree rounds
    key0 = keySchedules(masterkey, 0)
    keywhitening = xor(girdi,key0 ,4)
    round1 = cipher1round(keywhitening,keySchedules(masterkey,1),sbox2,perm1)
    round2 = cipher1round(round1, keySchedules(masterkey, 2),sbox2,perm1)
    round3 = cipher1round(round2, keySchedules(masterkey, 3),sbox2,perm1)
    round4 = xor(round3,keySchedules(masterkey,4),4)
    # Last round S-box
    for i in range(0, 4):
        round41[i] = sbox2[round4[i]]
    cikti = xor(round41,keySchedules(masterkey,5),4)
    return cikti

def cipher3(girdi, masterkey):
    # Define empty arrays
    round1 = [0] * 4; round2 = [0] * 4
    round3 = [0] * 4; round4 = [0] * 4
    round41 = [0] * 4; cikti = [0] * 4
    key0 = [0] * 4

    # First tree rounds
    key0 = keySchedules(masterkey, 0)
    keywhitening = xor(girdi,key0 ,4)
    round1 = cipher1round(keywhitening,keySchedules(masterkey,1),sbox2,perm2)
    round2 = cipher1round(round1, keySchedules(masterkey, 2),sbox2,perm2)
    round3 = cipher1round(round2, keySchedules(masterkey, 3),sbox2,perm2)
    round4 = xor(round3,keySchedules(masterkey,4),4)
    # Last round S-box
    for i in range(0, 4):
        round41[i] = sbox2[round4[i]]
    cikti = xor(round41,keySchedules(masterkey,5),4)
    return cikti

def dif_crypt_cipher1(anahtar):

    count=0
    reverse_sbox_output_one=[0,0,0,0]
    reverse_sbox_output_two=[0,0,0,0]
    reverse_key_xorb=[0,0,0,0]
    reverse_key_xora=[0,0,0,0]
    number_of_pairs=4096
    input_differential=[0,0,1,0]

    plaintexts = open("Plaintexts5000.txt", "w")
    d_plaintexts = open("Differential Plaintexts5000.txt", "w")
    encrypted_plaintexts = open("Encrypted plaintexts5000.txt", "w")
    d_encrypted_plaintexts = open("Differential Encrypted plaintexts5000.txt", "w")

    for i in range(number_of_pairs):
        plaintext = random_key()

        # writes Plaintexts to the text file
        for ele in plaintext:
            plaintexts.write(str(ele) + " ")
        plaintexts.write("\n")

        # writes plaintext which satisfy differential
        d_plaintext=xor(plaintext,input_differential,4)
        for ele in d_plaintext:
            d_plaintexts.write(str(ele)+ " ")
        d_plaintexts.write("\n")

        # writes Ciphertexts to the text file
        for ele in cipher1(plaintext,anahtar):
            encrypted_plaintexts.write(str(ele) + " ")
        encrypted_plaintexts.write("\n")

        # writes corresponding differential ciphertext
        for ele in cipher1(d_plaintext,anahtar):
            d_encrypted_plaintexts.write(str(ele)+ " ")
        d_encrypted_plaintexts.write("\n")

    encrypted_plaintexts.close()
    plaintexts.close()
    d_plaintexts.close()
    d_encrypted_plaintexts.close()


    max_count=0
    k=0
    kk=0
    for key1 in range(16):

        for key2 in range(16):
            count = 0
            # Open files for each key candidate
            ciphertexts_one = open("Encrypted plaintexts5000.txt", "r")
            ciphertexts_two = open("Differential Encrypted plaintexts5000.txt", "r")

            for line_one, line_two in zip(ciphertexts_one, ciphertexts_two):

                # puts elements in the line of the text in a array
                ciphertextlist_one = line_one.split(" ")
                ciphertextlist_two = line_two.split(" ")
                # deletes empty element of the list
                del ciphertextlist_one[4]
                del ciphertextlist_two[4]
                # Converts strings to int

                for i, j in zip(range(0, len(ciphertextlist_one)), range(0, len(ciphertextlist_two))):
                    ciphertextlist_one[i] = int(ciphertextlist_one[i])
                    ciphertextlist_two[i] = int(ciphertextlist_two[i])
                # Makes XOR between ciphertext and key candidate
                key_xora = xor(ciphertextlist_one, [0, key1, key2, 0],4)

                key_xorb = xor(ciphertextlist_two, [0, key1, key2, 0],4)

                # Puts result to inverse S-box

                reverse_sbox_out1 = s_box_inverse(key_xora,reverse_sbox1)
                reverse_sbox_out2 = s_box_inverse(key_xorb,reverse_sbox1)
                # Calculates differential
                diff = xor(reverse_sbox_out1, reverse_sbox_out2,4)
                # Checks if pair is right pair
                if (diff[0] == 0) and (diff[1] == 12) and (diff[2] == 12) and (diff[3] == 0):
                    count += 1

            # Find max count and keys
            if count > max_count:
                max_count = count
                k = key1
                kk = key2
            print("key1:{} key2:{} Count : {}".format(key1, key2, count ))
            ciphertexts_one.close()
            ciphertexts_two.close()

    print("------------------------------------------\n Last key : {} \n".format(keySchedules(anahtar,5)))
    print("Max count: {} at key1 : {}  key2 : {} , Prob : {} \n".format(max_count, k, kk , max_count/number_of_pairs))

def dif_crypt_cipher2(anahtar):

    count=0
    reverse_sbox_output_one=[0,0,0,0]
    reverse_sbox_output_two=[0,0,0,0]
    reverse_key_xorb=[0,0,0,0]
    reverse_key_xora=[0,0,0,0]
    number_of_pairs=4096
    input_differential=[0,0,6,0]

    plaintexts = open("Plaintexts5000.txt", "w")
    d_plaintexts = open("Differential Plaintexts5000.txt", "w")
    encrypted_plaintexts = open("Encrypted plaintexts5000.txt", "w")
    d_encrypted_plaintexts = open("Differential Encrypted plaintexts5000.txt", "w")

    for i in range(number_of_pairs):
        plaintext = random_key()

        # writes Plaintexts to the text file
        for ele in plaintext:
            plaintexts.write(str(ele) + " ")
        plaintexts.write("\n")

        # writes plaintext which satisfy differential
        d_plaintext=xor(plaintext,input_differential,4)
        for ele in d_plaintext:
            d_plaintexts.write(str(ele)+ " ")
        d_plaintexts.write("\n")

        # writes Ciphertexts to the text file
        for ele in cipher2(plaintext,anahtar):
            encrypted_plaintexts.write(str(ele) + " ")
        encrypted_plaintexts.write("\n")

        # writes corresponding differential ciphertext
        for ele in cipher2(d_plaintext,anahtar):
            d_encrypted_plaintexts.write(str(ele)+ " ")
        d_encrypted_plaintexts.write("\n")

    encrypted_plaintexts.close()
    plaintexts.close()
    d_plaintexts.close()
    d_encrypted_plaintexts.close()


    max_count=0
    k=0
    kk=0
    for key1 in range(16):

        for key2 in range(16):
            count = 0
            # Open files for each key candidate
            ciphertexts_one = open("Encrypted plaintexts5000.txt", "r")
            ciphertexts_two = open("Differential Encrypted plaintexts5000.txt", "r")

            for line_one, line_two in zip(ciphertexts_one, ciphertexts_two):

                # puts elements in the line of the text in a array
                ciphertextlist_one = line_one.split(" ")
                ciphertextlist_two = line_two.split(" ")
                # deletes empty element of the list
                del ciphertextlist_one[4]
                del ciphertextlist_two[4]
                # Converts strings to int

                for i, j in zip(range(0, len(ciphertextlist_one)), range(0, len(ciphertextlist_two))):
                    ciphertextlist_one[i] = int(ciphertextlist_one[i])
                    ciphertextlist_two[i] = int(ciphertextlist_two[i])
                # Makes XOR between ciphertext and key candidate
                key_xora = xor(ciphertextlist_one, [0, key1, key2, 0],4)

                key_xorb = xor(ciphertextlist_two, [0, key1, key2, 0],4)

                # Puts result to inverse S-box

                reverse_sbox_out1 = s_box_inverse(key_xora,reverse_sbox2)
                reverse_sbox_out2 = s_box_inverse(key_xorb,reverse_sbox2)
                # Calculates differential
                diff = xor(reverse_sbox_out1, reverse_sbox_out2,4)
                # Checks if pair is right pair
                if (diff[0] == 0) and (diff[1] == 12) and (diff[2] == 12) and (diff[3] == 0):
                    count += 1

            # Find max count and keys
            if count > max_count:
                max_count = count
                k = key1
                kk = key2
            print("key1:{} key2:{} Count : {}".format(key1, key2, count ))
            ciphertexts_one.close()
            ciphertexts_two.close()

    print("------------------------------------------\n Last key : {} \n".format(keySchedules(anahtar,5)))
    print("Max count: {} at key1 : {}  key2 : {} , Prob : {} \n".format(max_count, k, kk , max_count/number_of_pairs))

def dif_crypt_cipher3(anahtar):

    count=0
    reverse_sbox_output_one=[0,0,0,0]
    reverse_sbox_output_two=[0,0,0,0]
    reverse_key_xorb=[0,0,0,0]
    reverse_key_xora=[0,0,0,0]
    number_of_pairs=10000

    input_differential=[0,0,12,12]

    plaintexts = open("Plaintexts5000.txt", "w")
    d_plaintexts = open("Differential Plaintexts5000.txt", "w")
    encrypted_plaintexts = open("Encrypted plaintexts5000.txt", "w")
    d_encrypted_plaintexts = open("Differential Encrypted plaintexts5000.txt", "w")

    for i in range(number_of_pairs):
        plaintext = random_key()

        # writes Plaintexts to the text file
        for ele in plaintext:
            plaintexts.write(str(ele) + " ")
        plaintexts.write("\n")

        # writes plaintext which satisfy differential
        d_plaintext=xor(plaintext,input_differential,4)
        for ele in d_plaintext:
            d_plaintexts.write(str(ele)+ " ")
        d_plaintexts.write("\n")

        # writes Ciphertexts to the text file
        for ele in cipher2(plaintext,anahtar):
            encrypted_plaintexts.write(str(ele) + " ")
        encrypted_plaintexts.write("\n")

        # writes corresponding differential ciphertext
        for ele in cipher2(d_plaintext,anahtar):
            d_encrypted_plaintexts.write(str(ele)+ " ")
        d_encrypted_plaintexts.write("\n")

    encrypted_plaintexts.close()
    plaintexts.close()
    d_plaintexts.close()
    d_encrypted_plaintexts.close()


    max_count=0
    k=0
    kk=0
    for key1 in range(16):

        for key2 in range(16):
            count = 0
            # Open files for each key candidate
            ciphertexts_one = open("Encrypted plaintexts5000.txt", "r")
            ciphertexts_two = open("Differential Encrypted plaintexts5000.txt", "r")

            for line_one, line_two in zip(ciphertexts_one, ciphertexts_two):

                # puts elements in the line of the text in a array
                ciphertextlist_one = line_one.split(" ")
                ciphertextlist_two = line_two.split(" ")
                # deletes empty element of the list
                del ciphertextlist_one[4]
                del ciphertextlist_two[4]
                # Converts strings to int

                for i, j in zip(range(0, len(ciphertextlist_one)), range(0, len(ciphertextlist_two))):
                    ciphertextlist_one[i] = int(ciphertextlist_one[i])
                    ciphertextlist_two[i] = int(ciphertextlist_two[i])
                # Makes XOR between ciphertext and key candidate
                key_xora = xor(ciphertextlist_one, [0, 0, key1, key2],4)

                key_xorb = xor(ciphertextlist_two, [0, 0, key1, key2],4)

                # Puts result to inverse S-box

                reverse_sbox_out1 = s_box_inverse(key_xora,reverse_sbox2)
                reverse_sbox_out2 = s_box_inverse(key_xorb,reverse_sbox2)
                # Calculates differential
                diff = xor(reverse_sbox_out1, reverse_sbox_out2,4)
                # Checks if pair is right pair
                if (diff[0] == 0) and (diff[1] == 0) and (diff[2] == 2) and (diff[3] == 2):
                    count += 1

            # Find max count and keys
            if count > max_count:
                max_count = count
                k = key1
                kk = key2
            print("key1:{} key2:{} Count : {}".format(key1, key2, count ))
            ciphertexts_one.close()
            ciphertexts_two.close()

    print("------------------------------------------\n Last key : {} \n".format(keySchedules(anahtar,5)))
    print("Max count: {} at key1 : {}  key2 : {} , Prob : {} \n".format(max_count, k, kk , max_count/number_of_pairs))

if __name__ == '__main__':
    while True:
        a = input(
            "1 - DDT \n2 - Attack on Cipher 1 \n3 - Attack on Cipher 2 \n4 - Attack on Cipher 3 \n5 - Quit\nGo to : ")
        if a == str(1):
            b=input("Which S-box(1 or 2): ")
            if b == '1' :
                print_ddt(sbox1,4)
            if b == '2' :
                print_ddt(sbox2,4)
        if a == str(2):
            dif_crypt_cipher1(random_key())
        if a == str(3):
            dif_crypt_cipher2(random_key())
        if a == str(4):
            dif_crypt_cipher3(random_key())
        if a == str(5):
            break