
import time
import hashlib
import random
import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import pandas as pd

# Benchmark results storage
benchmark_results = {}

# -------------------------- Scheme 13: ECC-Based Redaction -------------------------- #
def ecc_generate_keys():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    return private_key, public_key

def ecc_sign_data(private_key, data):
    return private_key.sign(data.encode(), ec.ECDSA(hashes.SHA256()))

def ecc_verify_signature(public_key, data, signature):
    try:
        public_key.verify(signature, data.encode(), ec.ECDSA(hashes.SHA256()))
        return True
    except:
        return False

# Timing ECC-Based Redaction
start_time = time.perf_counter()
private_key, public_key = ecc_generate_keys()
signature = ecc_sign_data(private_key, "Sensitive Data")
is_valid = ecc_verify_signature(public_key, "Sensitive Data", signature)
end_time = time.perf_counter()
benchmark_results["ECC-Based Redaction"] = end_time - start_time

# -------------------------- Scheme 14: Multiplicative Hash -------------------------- #
def multiplicative_hash(data, key):
    return int.from_bytes(hashlib.sha256((data + str(key)).encode()).digest(), 'big')

def multiplicative_redact(data, key):
    return multiplicative_hash("REDACTED", key)

# Timing Multiplicative Hash
start_time = time.perf_counter()
key = random.randint(1, 2**256)
hash_value = multiplicative_hash("Sensitive Data", key)
redacted_hash = multiplicative_redact("Sensitive Data", key)
end_time = time.perf_counter()
benchmark_results["Multiplicative Hash"] = end_time - start_time

# -------------------------- Scheme 21: Attribute-Based Encryption (ABE) -------------------------- #
def generate_symmetric_key():
    return os.urandom(32)

def encrypt_data(key, plaintext):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padded_plaintext = plaintext.ljust(32).encode()  # Padding for AES
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return iv + ciphertext

def decrypt_data(key, ciphertext):
    iv = ciphertext[:16]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(ciphertext[16:]) + decryptor.finalize()
    return decrypted.strip()

# Timing ABE (AES-Based Simulation)
start_time = time.perf_counter()
abe_key = generate_symmetric_key()
ciphertext = encrypt_data(abe_key, "Sensitive Data")
decrypted = decrypt_data(abe_key, ciphertext)
end_time = time.perf_counter()
benchmark_results["ABE-Based Redaction"] = end_time - start_time

# -------------------------- Chameleon Hash (Your Scheme) -------------------------- #
def generate_trapdoor():
    return random.randint(1, 2**256)

def chameleon_hash(data, trapdoor):
    prime = 2**256 - 429
    data_int = int.from_bytes(hashlib.sha256(data.encode()).digest(), 'big')
    return (data_int ^ trapdoor) % prime

def create_collision(original_data, redacted_data, trapdoor):
    prime = 2**256 - 429
    original_int = int.from_bytes(hashlib.sha256(original_data.encode()).digest(), 'big')
    redacted_int = int.from_bytes(hashlib.sha256(redacted_data.encode()).digest(), 'big')
    return (original_int ^ trapdoor) ^ redacted_int

# Timing Chameleon Hash
start_time = time.perf_counter()
trapdoor = generate_trapdoor()
original_hash = chameleon_hash("Sensitive Data", trapdoor)
new_trapdoor = create_collision("Sensitive Data", "REDACTED", trapdoor)
new_hash = chameleon_hash("REDACTED", new_trapdoor)
end_time = time.perf_counter()
benchmark_results["Chameleon Hash Redaction"] = end_time - start_time

# -------------------------- Display Results -------------------------- #
df = pd.DataFrame(benchmark_results.items(), columns=["Redaction Scheme", "Time (seconds)"])
print(df)
