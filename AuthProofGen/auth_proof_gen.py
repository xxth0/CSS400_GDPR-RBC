import time
import hashlib
import sympy
import random
from ecdsa import SigningKey, NIST256p

# RSA Authentication (Simulating Work [2])
def rsa_authentication():
    start_time = time.time()
    p = sympy.randprime(2**511, 2**512)
    q = sympy.randprime(2**511, 2**512)
    n = p * q
    e = 65537
    phi = (p-1) * (q-1)
    d = pow(e, -1, phi)
    message = b"auth_request"
    hashed = int(hashlib.sha256(message).hexdigest(), 16)
    signature = pow(hashed, d, n)
    auth_time = time.time() - start_time
    return auth_time

# ECC Authentication (Simulating Work [13])
def ecc_authentication():
    start_time = time.time()
    sk = SigningKey.generate(curve=NIST256p)
    message = b"auth_request"
    signature = sk.sign(message)
    auth_time = time.time() - start_time
    return auth_time

# Quantum Key Distribution (Simulating Work [6])
def qkd_authentication():
    start_time = time.time()
    key_bits = [random.randint(0, 1) for _ in range(256)]
    auth_time = time.time() - start_time
    return auth_time
