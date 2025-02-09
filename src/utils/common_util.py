import base64
import math
import random
import string

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


def random_str_by_len(len_=10, /) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=len_))


def decode_base64(data) -> str:
    return base64.b64decode(data).decode("utf-8")


def encrypt_rsa_base64(raw_msg, keypath):
    if isinstance(keypath, bytes) or isinstance(keypath, str):
        publickey = keypath
    else:
        with open(keypath, "rb") as f:
            publickey = f.read()

    pubKeyObj = RSA.importKey(publickey)
    cipher = PKCS1_v1_5.new(pubKeyObj)

    if isinstance(raw_msg, bytes):
        msg = raw_msg
    else:
        msg = raw_msg.encode("utf-8")
    emsg = cipher.encrypt(msg)
    return base64.b64encode(emsg).decode("utf-8")


def calculate_percentile(data, percentile):
    if not data:
        raise ValueError("Data list cannot be empty")
    if not (0 <= percentile <= 100):
        raise ValueError("Percentile must be between 0 and 100")

    # Sort the data
    data.sort()

    # Compute the index (percentile position)
    index = (percentile / 100) * (len(data) - 1)
    lower_idx = math.floor(index)
    upper_idx = math.ceil(index)

    # If index is an integer, return the exact value
    if lower_idx == upper_idx:
        return data[int(index)]

    # Otherwise, interpolate between two closest values
    lower_value = data[lower_idx]
    upper_value = data[upper_idx]
    return round(lower_value + (upper_value - lower_value) * (index - lower_idx), 3)
