import base64
import random
from Crypto.Cipher import AES


def add_to_16(data: str) -> bytes:
    data_bytes = data.encode('utf-8')
    if len(data) % 16:
        add = 16 - (len(data_bytes) % 16)
    else:
        add = 0
    return data_bytes + (b'\0' * add)


def encrypt_by_aes(data: str, iv: str, key: str = 'root%$#@!1234567') -> str:
    key = key.encode('utf-8')
    data = add_to_16(data)
    cryptos = AES.new(key, AES.MODE_CBC, iv.encode('utf-8'))
    cipher_data = cryptos.encrypt(data)
    return base64.standard_b64encode(cipher_data).decode('utf-8')+iv


def decrypt_by_aes(text: str, key: str = 'root%$#@!1234567'):
    key = key.encode('utf-8')
    iv = text[-16:]
    data = text[:-16]
    data = data.encode('utf-8')
    data = base64.b64decode(data)
    cryptos = AES.new(key, AES.MODE_CBC, iv.encode('utf-8'))
    cipher_data = cryptos.decrypt(data)
    return cipher_data.decode('utf-8').strip('\0')


def get_rand_num() -> str:
    digits = [str(i) for i in range(10)]
    lowers = [chr(i) for i in range(65, 91)]
    uppers = [chr(i) for i in range(97, 123)]
    chars = digits+lowers+uppers
    nums = ''
    for i in range(16):
        idx = random.randint(0, 61)
        nums += chars[idx]
    return nums


if __name__ == '__main__':
    data = 'hello'
    iv = get_rand_num()
    text = encrypt_by_aes(data, iv)
    print(text)
    temp = decrypt_by_aes(text)
    assert temp == data
