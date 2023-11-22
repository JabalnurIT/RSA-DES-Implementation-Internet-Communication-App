import socketio
import eventlet
from des import DES
from utils import Utils


des = DES()
utils = Utils()

sio = socketio.Server()
app = socketio.WSGIApp(sio)


# Fungsi enkripsi DES
def encrypt(text, key):
    key = key.upper()

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

    pt_all = utils.string_to_hexadecimal(text).upper()
    pt_chunks = [pt_all[i:i + 16] for i in range(0, len(pt_all), 16)]
    if len(pt_chunks[-1]) % 16 != 0:
        while len(pt_chunks[-1]) % 16 != 0:
            pt_chunks[-1] += "20"

    cipher_text_all = ""

    for i,pt in enumerate(pt_chunks):
        cipher_text_hexa = utils.bin2hex(des.encrypt(pt, rkb, rk))
        cipher_text = utils.hexadecimal_to_string(cipher_text_hexa)
        cipher_text_all += cipher_text

    return cipher_text_all

# Fungsi dekripsi DES
def decrypt(text, key):
    key = key.upper()

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
    
    cipher_text_hexa_all = utils.string_to_hexadecimal(text).upper()
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

    return text_all

# Daftar klien yang terhubung
clients = {}

@sio.event
def connect(sid, environ):
    print(f"Client {sid} connected")

@sio.event
def disconnect(sid):
    print(f"Client {sid} disconnected")
    # Menghapus informasi tentang klien yang terputus
    clients.pop(sid, None)

@sio.event
def send_message(sid, data):
    sender_sid = sid
    text = data['text']
    key = data['key']
    recipient_sid = data['recipient_sid']
    
    # Encrypt the message before sending
    encrypted_text = encrypt(text, key)
    
    # Kirim pesan terenkripsi ke klien penerima
    for client_sid, client_info in clients.items():
        if client_sid == recipient_sid:
            sio.emit('receive_message', {'sender_sid': sender_sid, 'encrypted_text': encrypted_text}, room=client_sid)
            break

@sio.event
def set_username(sid, data):
    # Mendapatkan nama pengguna dari klien
    username = data.get('username')
    if username:
        # Menambahkan informasi klien ke dalam daftar
        clients[sid] = {'sid': sid, 'username': username}
        print(f"Client {sid} set username to {username}")

@sio.event
def get_user_list(sid):
    # Mengirim daftar pengguna dan sid yang terhubung ke klien
    user_list = [{'username': client_info['username'], 'sid': client_info['sid']} for client_sid, client_info in clients.items()]
    # Print user list
    user_send = []
    for user in user_list:
        if user['sid'] != sid:
            user_send.append(user)
    sio.emit('user_list', {'users': user_send}, room=sid)

@sio.event
def get_message(sid, data):

    decrypted_text = decrypt(data['text'], data['key'])
    sio.emit('open_message', {'username': data['sender_username'], 'text':decrypted_text}, room=sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 8888)), app)