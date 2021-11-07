import base64
from Crypto.Cipher import AES
from config import *


# AES256-CBC Encryption
class AESCipher(object):
    def __init__(self, key):
        self.bs = 32
        self.PADDING = "#".encode('utf8')
        self.key = key[:32]
        # print('key = ' ,self.key)
        self.IV = '\x00'.encode('utf8') * 16

    def encrypt(self, raw):
        raw = self._pad(raw.encode('utf8'))
        iv = self.IV
        cipher = AES.new(self.key.encode('utf8'), AES.MODE_CBC, iv)
        return base64.b64encode(cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = self.IV
        cipher = AES.new(self.key.encode('utf8'), AES.MODE_CBC, iv)
        return cipher.decrypt(enc).rstrip(bytes(self.PADDING))

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * self.PADDING

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


def aes256cbc_encrypt(rawdata):
    a = AESCipher(AES256_KEY)
    enc_data = a.encrypt(rawdata)
    return enc_data


if __name__ == "__main__":
    aes256cbc_encrypt("Hello")
