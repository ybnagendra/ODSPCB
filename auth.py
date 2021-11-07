import rsa
import base64
import pytz
import datetime
from base64 import b64decode
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from cfasf import *


# Function to encrypt keys(public_key and private_key).
def enc_keys(pbk, pvk):
    key64 = pbk.encode()
    key = b64decode(key64)  # key is in bytes \xf5
    key = RSA.importKey(key)  # Return key object address
    public_modulus = key.publickey()  # Used for authorization

    key256 = pvk.encode()
    key_der_pri = b64decode(key256)
    key = RSA.importKey(key_der_pri)
    private = PKCS1_v1_5.new(key)      # Used for signature
    return public_modulus, private


# Function to return authorization, signature and timestamp  for SPCB Realtime and Delayed Upload
# Inputs server_public_key and site_private_key
# To generate Authorization, site public key shall be provided.
# To generate Signature, site private key shall be provided.
# Input message to encrypt site_id^ver1.0^timestamp
# Sample Message ex:site_2944^ver1.0^2020-12-30T12:47:00Z
# Timestamp must be Real time
def spcb_authorization():
    now_utc = datetime.datetime.utcnow()
    local_tz = pytz.timezone('Asia/Kolkata')  # Local timezone which we want to convert the UTC time
    now_utc = pytz.utc.localize(now_utc)  # Add timezone information to UTC time
    x = now_utc.astimezone(local_tz)  # Convert to local time
    timestamp = x.strftime('%Y-%m-%dT%H:%M:00Z')
    # print("TimeStamp of RSA Message :", timestamp)

    rsa_msg = site_id+'^'+version+'^'+'{}'.format(timestamp)
    public_mod, private = enc_keys(server_public_key, site_private_key)
    # print("RSA Message :", rsa_msg)
    crypto = rsa.encrypt(rsa_msg.encode(), public_mod)
    rsa_auth = base64.b64encode(crypto)
    authorization = rsa_auth.decode('ascii')

    hash_address = SHA256.new(rsa_msg.encode("utf8"))
    rsa_sign_raw = private.sign(hash_address)
    rsa_sign = base64.b64encode(rsa_sign_raw)
    signature = rsa_sign.decode('ascii')
    return authorization, signature, timestamp


# Function to return authorization, signature and timestamp  for CPCB Realtime and Delayed Upload
# Inputs site_public_key and site_private_key
# To generate Authorization, site public key shall be provided.
# To generate Signature, site private key shall be provided.
# Input message to encrypt site_id^ver1.0^timestamp
# Sample Message ex:site_2944^ver1.0^2020-12-30T12:47:00Z
# Timestamp must be Real time
def cpcb_authorization():
    now_utc = datetime.datetime.utcnow()
    local_tz = pytz.timezone('Asia/Kolkata')  # Local timezone which we want to convert the UTC time
    now_utc = pytz.utc.localize(now_utc)  # Add timezone information to UTC time
    x = now_utc.astimezone(local_tz)  # Convert to local time
    timestamp = x.strftime('%Y-%m-%dT%H:%M:00Z')
    # print("TimeStamp of RSA Message :", timestamp)

    rsa_msg = site_id+'^'+version+'^'+'{}'.format(timestamp)
    public_mod, private = enc_keys(site_public_key, site_private_key)
    # print("RSA Message :", rsa_msg)
    crypto = rsa.encrypt(rsa_msg.encode(), public_mod)
    rsa_auth = base64.b64encode(crypto)
    authorization = rsa_auth.decode('ascii')

    hash_address = SHA256.new(rsa_msg.encode("utf8"))
    rsa_sign_raw = private.sign(hash_address)
    rsa_sign = base64.b64encode(rsa_sign_raw)
    signature = rsa_sign.decode('ascii')
    return authorization, signature, timestamp


if __name__ == "__main__":
    spcb_authorization()
    cpcb_authorization()

