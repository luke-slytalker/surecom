# embed data into an image (takes JPG or PNG, outputs PNG)
# USAGE:  embed.py -i IMAGE -d DATA [-p PASSWORD] [-s SAVE_AS] [-o OFFSET]
#       IMAGE:  cover image
#       DATA:   data to embed into image
#       PASSWORD:   password to lock/unlock
#       SAVE_AS:    name to save steg'ed file as
#       OFFSET:     embedding offset (for further obfuscation)

from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from stegano import lsb
from ciphers import lukefuscate, unlukefuscate
import argparse

parser = argparse.ArgumentParser(description='SURECOM // \n'
                                             'Super Ultra Reliable Exfiltration & Communications Obfuscator Machine ')

# cover image to use
parser.add_argument('-i', action="store", dest="img", required=True, help="Path to cover image")
# data string to embed
parser.add_argument('-d', action="store", dest="data", required=True, help="The string of data you want to encrypt & steganographyically embed into an image")
# steg'ed image (where to save)
parser.add_argument('-s', action="store", dest="steg", default="steg-image.png", help="What to save your steg'ed image as")
# password to use
parser.add_argument('-p', action="store", dest="password", default="3NCRYPT10N3D", help="A password to use for encrypting & embedding \n(default: 3NCRYPT10N3D")
# offset
parser.add_argument('-o', action="store", dest="offset", type=int, default=17, help="offset of embedding; a way to obfuscate the stego (default: 17)")
## eXtra obfuscation
#parser.add_argument('-x', action="store", dest="extra", type=bool, default=False, help="Add eXtra obfuscation to the steganographic embedding")


comms = parser.parse_args()

offset = comms.offset       # offset to embed at
inp = comms.data            # input data to encrypt & embed
password = comms.password   # password to use
img = comms.img             # cover image
saveas = comms.steg         # what to save the steg'ed image as


def embed(img, saveas, password, inp, offset):
    # encrypt & embed a data string into an image
    salt = get_random_bytes(16)             # generate something salty..
    key = PBKDF2(password, salt, dkLen=16)  # encryption key generated from the password

    cipher = AES.new(key, AES.MODE_CBC)                     # let's get encrypting...
    data = inp.encode()                                     # encode input to a bytes object
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))    # cipher text bytes
    iv = b64encode(cipher.iv).decode('utf-8')               # base64 encoded IV
    ct = b64encode(ct_bytes).decode('utf-8')                # base64 encoded Cipher Text
    salt_s = b64encode(salt).decode('utf-8')                # base64 encoded Salt

    enc_string = lukefuscate(salt_s + iv + ct)      # obfuscation/substitution cipher

    steg_it = lsb.hide(img, enc_string, encoding="UTF-8", shift=offset, auto_convert_rgb=True)

    steg_it.save(saveas)        # save the image
    return "SAVED AS:  " + str(saveas)


did_it_work = embed(img, saveas, password, inp, offset)
print(did_it_work)

