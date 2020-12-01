import json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
#from Crypto.Random import get_random_bytes

PADDING = '#'
BLOCK_SIZE = 16
padw = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

output_file = 'encrypted.dat' # Output file

key = b'c2l0ZV8zMDE3XnZlcl8xLjBeT1NQQ0Je' # The key you generated
iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


f = open('rawdata.txt')
data1= f.read()
f.close()

#data = data1.encode()           #convert string to bytes
padd = padw(data1)              # Padding the data with #
padb = padd.encode()            #convert string to bytes
#print(padb)

# Create cipher object and encrypt the data
cipher = AES.new(key, AES.MODE_CBC,iv=iv) # Create a AES cipher object with the key using the mode CBC
#AES.block_size =32         #Encryption is working
AES.block_size =16
ciphered_data = cipher.encrypt(pad(padb, AES.block_size)) # Pad the input data and then encrypt
print(AES.block_size)
print(ciphered_data)
############################################################
print("\nbase64 encode")
iv = b64encode(cipher.iv).decode('utf-8')
ct = b64encode(ciphered_data).decode('utf-8')
print(iv)
print(ct)
#############################################################

file_out = open(output_file, "wb") # Open file to write bytes
file_out.write(cipher.iv) # Write the iv to the output file (will be required for decryption)
file_out.write(ciphered_data) # Write the varying length ciphertext to the file (this is the encrypted data)
file_out.close()

result = json.dumps({'iv':iv, 'ciphertext':ct})
print(result)


try:
    b64 = json.loads(result)
    iv = b64decode(b64['iv'])
    ct = b64decode(b64['ciphertext'])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    print("The Decrypted message was: \n ", pt.decode())
except ValueError or KeyError:
    print("Incorrect decryption")







