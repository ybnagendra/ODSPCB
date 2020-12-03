import os, time
import sys
import codecs

import rsa

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


#from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import binascii
import base64
from base64 import b64decode
from base64 import b64encode



global rsa_auth,rsa_sign
rsa_auth = "RSA_AUTHORIZATION"
rsa_sign = "RSA_SIGNATURE"

site_id  = "site_3069"
rest_12  = "20200306163100"
filename = "site_3069_SMS_20200306163000"
file_data_buffer = []


def get_time():
    t = time.strftime('%Y-%m-%dT:%I:%M:00', time.localtime())
    message = '{}^ver1.0^{}'.format(site_id, t)
    return message
    

def rsa_auth_string(message):
    global rsa_auth

    #key64 = b'MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJhYF7Y8wxNVgjP+EfA4YNIdY0DCjgajTRJjeud+X5VPL4RPc7s4d0+VeO0w3C3vOzafcwIMaMKfS6pWmo32g3ECAwEAAQ=='
    key64 = b'MEgCQQCO8qduFvXPyt3qeJBQjhQ3CkMD Njj+oVOkXxfu7EKjo8GyuzfGaOs1+zj+\niNcPFehf8o0nywl2UR/PsH7D+PWvAgMBAAE='


    key = b64decode(key64)
    key = RSA.importKey(key)
    publickey = key.publickey()

    crypto = rsa.encrypt(message.encode(), publickey)
    rsa_auth = base64.b64encode(crypto)
    #print(rsa_auth)
    #print(len(rsa_auth))

    '''
    key256 = b'MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAhs0v9TVZJZCVf+cpJoiNiPr+16CAgwnhYUJvyJuF0effI+VpTaldwmk7wANcTt5E5eINdmrrXBPjX1ePuII0kQIDAQABAkBol5hYaBZNYUu+O/vf3CAFYsqNQAm2otnu/v+A5bsFS/lW5miLV43CaIKBoR7VrNqUkwf69beu82iQJSFYGHKBAiEA+NakJUOsakwiMlPcwyUfZ/duy+68L8DUt13/N4yMzXkCIQCKrlwplFLAhiUFCrTeV4zcI44ge/Gd6PuSfPEH3dsR2QIgGeIxxtKIP7JVqEiC4SWeY7EgLERT/N+hAMXdQ0jyaHkCIQCD87UDZvp57ulIa9B+ggUn7Lit1eCmpGjCEBlyp7hquQIge2CiYZK0OD4StZMApqtpz8edXUPmk9WvTGui0zwFAkA='
    keyDER_pri = b64decode(key256)
    keyDER_pri = RSA.importKey(keyDER_pri)
    message = rsa.decrypt(crypto, keyDER_pri)
    print(message.decode('utf8'))
    '''
    

def rsa_signature(message):
    global rsa_sign
    
    # Generate 1024-bit RSA key pair (private + public key)
    #keyPair = RSA.generate(bits=1024)
    #pubKey = keyPair.publickey()

    key256 = b'MIIBOw IBAAJBAI7yp24W9c/K3ep4kFCOFDcKQwM2OP6\
    hU6RfF+7sQqOjwbK7N8Zo\n6zX7OP6I1w8V6F/yjSfL CXZRH8+wfs\
    P49a8CAwEAAQJAWH6oYGMecjFpCMryrKwI\nn7pemhJrXleJbGziaC\
    si9ux8v1TQTuB4G+ vToiTYie/PDSaaaHLCxHLwTWS+AZHY\nAQIjA\
    LOlC79nRhyA8gus8rW0vebDSwPTGEo5wXCcgkWgD3xP QwECHwDLtK\
    mskSCW\n0IGp9RLELy9p/YQP9hNzN1gcBfFSKK8CIm8cezqkjrnci\
    1jrXKdEplxPmFtCOn jW\nZi3Xr7+Os2VIxQECHgHpXRpAdmTT6hO\
    VOCrdIn3FIkMgFQikwU/qAly6AwIiK1Sb\ni9yiepdrg9 S96O8F1x\
    Amb2eYbkJv94i6cTlHeHj4fQ=='

    keyDER_pri = b64decode(key256)
    key = RSA.importKey(keyDER_pri)
    privatekey = key.exportKey()
    #print(privatekey)

    # Sign the message using the PKCS#1 v1.5 signature scheme (RSASP1)
    hash = SHA256.new(message.encode("utf8"))
    signer = PKCS1_v1_5.new(key)
    rsa_sign_raw = signer.sign(hash)
    rsa_sign = base64.b64encode(rsa_sign_raw)
    #print(rsa_sign)
    #hexify = codecs.getencoder('hex')
    #m = hexify(rsa_sign_raw)[0]
    #print(m)

def http_message_body():
    global rsa_auth,rsa_sign
    
    file_wext = filename + ".zip"
    file_length = os.path.getsize(file_wext)
    with open(file_wext, "rb") as f:
     file_data_buffer = f.read()

    fdata_encoded = base64.b64encode(file_data_buffer)
    ht = "\r\n--WebKitFormBoundary7MA4YWxkTrZu0gW--\r\n";

    data =\
    '--WebKitFormBoundary7MA4YWxkTrZu0gW\r\n\
    Content-Disposition:form-data;name=\"file\";filename=\"{}\"\r\n\
    Content-Type:application/zip\r\n\
    \r\n{}'.format(filename,ht)

    k2=len(ht)+ len(data)

    header =\
    'POST http://ospcb-rtdas.com/OSPCBRTDASServer/realtimeUpload HTTP/1.1\r\n\
    Host:ospcb-rtdas.com\r\n\
    User-Agent:DTU\r\n\
    Authorization:Bearer {}\r\n\
    Signature:{}\r\n\
    siteId:{}\r\n\
    timestamp:{}\r\n\
    Content-Type:multipart/form-data;boundary=WebKitFormBoundary7MA4YWxkTrZu0gW\r\n\
    Content-Length: {}\
    \r\n\\r\n'.format(rsa_auth,rsa_sign,site_id,rest_12,k2)



    print(header)
    print(data)
    print(fdata_encoded)
    print(ht)
    

def main():
    msg_str = get_time()
    print(msg_str)
    rsa_auth_string(msg_str)
    rsa_signature(msg_str)
    http_message_body()

if __name__ == '__main__':
    main()
	

