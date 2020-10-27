# extract data from an image (PNG images only for extraction)
# USAGE:  extract.py -i IMAGE [-p PASSWORD] [-o OFFSET]
#       IMAGE:  image to (try and) extract data from
#       PASSWORD:   password to lock/unlock
#       OFFSET:     embedding offset

from stegano import lsb
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from ciphers import unlukefuscate
import argparse

parser = argparse.ArgumentParser(description='SURECOM // \n'
                                             'Super Ultra Reliable Exfiltration & Communications Obfuscator Machine ')
# image to extract data from
parser.add_argument('-i', action="store", dest="image", required=True, help="Path to image")
# password to use
parser.add_argument('-p', action="store", dest="password", default="3NCRYPT10N3D", help="The password to unlock the encryption & embedded data")
# offset
parser.add_argument('-o', action="store", dest="offset", type=int, default=17, help="offset of embedding")
## eXtra obfuscation
#parser.add_argument('-x', action="store", dest="extra", type=bool, default=False, help="Add eXtra obfuscation to the steganographic embedding")

comms = parser.parse_args()
if not comms.image:
    parser.print_help()
    quit()

img = comms.image
offset = comms.offset
password = comms.password


def extract(img, password, offset):
    # extract data from an image
    y = lsb.reveal(img, encoding="UTF-8", shift=offset)

    if y is None:
        return "Unable to retrieve any embedded data"

    x = unlukefuscate(y)

    s1 = x[:44]         # salt (first 44)
    s2 = x[44:68]       # Initialization Vector (next 24)
    s3 = x[68:]         # Cipher Text / encrypted message (rest of message)

    salt = b64decode(s1)  # base64 decoded salt
    iv = b64decode(s2)  # base64 decoded init vector
    ct = b64decode(s3)  # base64 decoded cipher text

    key = PBKDF2(password, salt, dkLen=32)  # Your key that you can encrypt with

    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode()
    except ValueError:
        return "Decryption failed"


msg = extract(img, password, offset)
print(msg)