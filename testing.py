
# import des and utils
from des import DES
from utils import Utils

des = DES()
utils = Utils()

# KEY
# while(True):
#   key_input = str(input("Masukkan key (16 digit Hexa 1-F): "))
#   input_key = key_input.upper()
#   if len(input_key) != 16:
#     print("Panjang key bukan 16 digit")
#   elif not utils.is_hexadecimal(input_key):
#     print("Terdapat angka yang bukan hexadecimal 1-F")
#   else:
#     break
key_input = '0987654321abcedf'

key = key_input.upper()

# Key generation
key = utils.hex2bin(key)

# --parity bit drop table
keyp = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

# Getting 56-bit key from 64-bit using the parity bits
key = des.permute(key, keyp, 56)

# Number of bit shifts
shift_table = [1, 1, 2, 2,
               2, 2, 2, 2,
               1, 2, 2, 2,
               2, 2, 2, 1]

# Key- Compression Table: Compression of key from 56 bits to 48 bits
key_comp = [14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32]

# Splitting
left = key[0:28]  # rkb for RoundKeys in binary
right = key[28:56]  # rk for RoundKeys in hexadecimal

rkb = []
rk = []
for i in range(0, 16):
    # Shifting the bits by nth shifts by checking from shift table
    left = des.shift_left(left, shift_table[i])
    right = des.shift_left(right, shift_table[i])

    # Combination of left and right string
    combine_str = left + right

    # Compression of key from 56 to 48 bits
    round_key = des.permute(combine_str, key_comp, 48)

    rkb.append(round_key)
    rk.append(utils.bin2hex(round_key))


# pt_input = input("Masukkan Text: ")
pt_input = 'Jabalnur adalah seorang kapiten ulung dari makassar'

# type_des = input("Encrypt(1)/Decrypt(2): ")

# if type_des == "1":
    # TEXT
pt_all = utils.string_to_hexadecimal(pt_input).upper()
pt_chunks = [pt_all[i:i + 16] for i in range(0, len(pt_all), 16)]
if len(pt_chunks[-1]) % 16 != 0:
    while len(pt_chunks[-1]) % 16 != 0:
        pt_chunks[-1] += "20"


cipher_text_all = ""
cipher_text_hexa_all = ""

for i,pt in enumerate(pt_chunks):
    cipher_text_hexa = utils.bin2hex(des.encrypt(pt, rkb, rk))
    cipher_text_hexa_all += cipher_text_hexa
    cipher_text = utils.hexadecimal_to_string(cipher_text_hexa)
    cipher_text_all += cipher_text

cipher_text_hexa_all_chunks = [cipher_text_hexa_all[i:i + 16] for i in range(0, len(cipher_text_hexa_all), 16)]
print("Cipher TextPlain:")
print("[START]", cipher_text_all, "[END]")


# elif type_des == "2":
    # TEXT
cipher_text_hexa_all = utils.string_to_hexadecimal(cipher_text_all).upper()
cipher_text_hexa_all_chunks = [cipher_text_hexa_all[i:i + 16] for i in range(0, len(cipher_text_hexa_all), 16)]

text_all = ""
text_hexa_all = ""

for i,cipher_text_hexa in enumerate(cipher_text_hexa_all_chunks):
    rkb_rev = rkb[::-1]
    rk_rev = rk[::-1]
    text_hexa = utils.bin2hex(des.encrypt(cipher_text_hexa, rkb_rev, rk_rev))
    text_hexa_all += text_hexa
    text = utils.hexadecimal_to_string(text_hexa)
    text_all += text

text_hexa_all_chunks = [text_hexa_all[i:i + 16] for i in range(0, len(text_hexa_all), 16)]
text_all = text_all.rstrip()
print('TextPlain:', text_all)