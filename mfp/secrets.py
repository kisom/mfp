"""
Secret sharing example. NOTE: insecure.
"""

import binascii
import struct

from mfp import poly


def random():
    s = open("/dev/urandom", "rb").read(4)
    n = struct.unpack("I", s)
    return n[0]


def generate_secret_key(k, n):
    secret = open("/dev/urandom", "rb").read(32)
    secret = int(binascii.hexlify(secret), 16)

    coeffs = []
    for i in range(k - 1):
        coeffs.append(random())

    print(coeffs)
    keys = []
    p = poly.Polynomial(coeffs, True)
    print(p)
    for i in range(1, n + 1):
        print(i, p(i))
        keys.append((i, p(i)))

    return keys


def reconstruct_secret(keys):
    p = poly.interpolate(keys)
    return p(0)
