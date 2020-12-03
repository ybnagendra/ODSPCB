#!/usr/bin/env python3
#
# This is a simple script to encrypt a message using AES
# with CBC mode in Python 3.
# Before running it, you must install pycryptodome:
#
# $ python -m pip install PyCryptodome
#
# Author.: José Lopes
# Date...: 2019-06-14
# License: MIT
##

from hashlib import md5
from base64 import b64decode
from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
#from Crypto.Random import get_random_bytes


PADDING = '#'
BLOCK_SIZE = 32
padw = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

class AESCipher:
    def __init__(self, key):
        self.key = md5(key.encode('utf8')).digest()

    def encrypt(self, data):
        iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        self.cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + self.cipher.encrypt(pad(data.encode('utf-8'), AES.block_size)))

    def encrypt1(self, data):
        iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        self.cipher = AES.new(self.key, AES.MODE_CBC, iv)
        AES.block_size = 32
        # print(AES.block_size)
        pad1 = padw(data)
        print(pad1)
        print("Encrypt1")
        return b64encode(iv + self.cipher.encrypt(pad(pad1.encode('utf-8'), AES.block_size)))


    def decrypt(self, data):
        raw = b64decode(data)
        self.cipher = AES.new(self.key, AES.MODE_CBC, raw[:AES.block_size])
        return unpad(self.cipher.decrypt(raw[AES.block_size:]), AES.block_size)

    def decrypt1(self, data):
        print("Decrypt 1->Block_Size=32")
        raw = b64decode(data)
        print(raw)
        iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        PADDING = '#'
        BLOCK_SIZE = 32
        padw = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

        self.cipher = AES.new(self.key, AES.MODE_CBC, raw[:32])
        return unpad(self.cipher.decrypt(raw[32:]), 32)

if __name__ == '__main__':
    print('TESTING ENCRYPTION')
    f = open('rawdata.txt')
    msg = f.read()
    f.close()

    pwd ="c2l0ZV8zMDE3XnZlcl8xLjBeT1NQQ0Je"

    #print('Ciphertext:', AESCipher(pwd).encrypt(msg).decode('utf-8'))
    print('Ciphertext:', AESCipher(pwd).encrypt(msg).decode('utf-8'))
    

    
    print('\nTESTING DECRYPTION')
    cte = AESCipher(pwd).encrypt(msg).decode('utf-8')
    print('Message...:', AESCipher(pwd).decrypt(cte).decode('utf-8'))
