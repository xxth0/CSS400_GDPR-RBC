import time
import os
import rsa
import gc
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from Crypto.PublicKey import ECC
import oqs
from Crypto.Cipher import AES

# File for testing
pdf_file = "C:\\Users\\WINDOWS\\Documents\\CSS400_GDPR-RBC\\cust-pdf\\experiment\\customer_1600KB.pdf"

def read_pdf(file_path):
    with open(file_path, "rb") as f:
        return f.read()

# Helper function for timing execution (microseconds)
def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return result, (end_time - start_time) * 1_000_000  # Convert to microseconds

# AES Encryption and Decryption (Csym)
def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return (cipher.nonce, ciphertext, tag, key)

def aes_decrypt(encrypted_data_tuple):
    nonce, ciphertext, tag, key = encrypted_data_tuple
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

# Hybrid RSA + AES Encryption and Decryption
rsa_pub, rsa_priv = rsa.newkeys(1024)

def hybrid_encrypt(data, rsa_pub_key):
    aes_key = os.urandom(32)  # Generate AES key
    encrypted_data = aes_encrypt(data, aes_key)  # Encrypt PDF with AES
    encrypted_aes_key = rsa.encrypt(aes_key, rsa_pub_key)  # Encrypt AES key with RSA
    return (encrypted_aes_key,) + encrypted_data  # Store both encrypted AES key and file

def hybrid_decrypt(encrypted_data, rsa_priv_key):
    encrypted_aes_key = encrypted_data[0]  # Extract encrypted AES key
    aes_key = rsa.decrypt(encrypted_aes_key, rsa_priv_key)  # Decrypt AES key
    encrypted_file_data = encrypted_data[1:]  # Extract encrypted file
    return aes_decrypt(encrypted_file_data)

# Post-Quantum Computing Encryption (PyCryptodome ECC + AES)
def pqc_encrypt(data):
    kem = oqs.KeyEncapsulation("Kyber1024")
    pk = kem.generate_keypair()
    cipher_text, shared_secret = kem.encapsulate(pk)
    aes_key = shared_secret[:32]  # Use part of shared secret as AES key
    cipher = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return (cipher_text, cipher.nonce, ciphertext, tag, kem.export_secret_key())

def pqc_decrypt(encrypted_data_tuple):
    cipher_text, nonce, ciphertext, tag, sk = encrypted_data_tuple
    kem = oqs.KeyEncapsulation("Kyber1024")
    kem.import_secret_key(sk)
    shared_secret = kem.decapsulate(cipher_text)
    aes_key = shared_secret[:32]
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

# ECC Scalar Multiplication (CECCScaMul) - Simulating ECC cost
def ecc_scalar_multiplication(point, scalar):
    key = ECC.generate(curve="P-256")
    return key.pointQ * scalar  # Real ECC multiplication

# User selects which scheme to test
print("Select a scheme to test:")
print("1: Hybrid RSA + AES")
print("2: QKD + PQC (PyCryptodome ECC + AES)")
print("3: ECC Scalar Multiplication")
print("4: C_sym (AES only)")

choice = input("Enter choice (1-4): ")

data = read_pdf(pdf_file)
if choice == "1":
    enc_result, enc_time = measure_time(hybrid_encrypt, data, rsa_pub)
    dec_result, dec_time = measure_time(hybrid_decrypt, enc_result, rsa_priv)
    print(f"[2] Hybrid RSA + AES | Encrypt Time: {enc_time:.3f} µs | Decrypt Time: {dec_time:.3f} µs")

elif choice == "2":
    enc_result, enc_time = measure_time(pqc_encrypt, data)
    dec_result, dec_time = measure_time(pqc_decrypt, enc_result)
    print(f"[6] QKD + PQC (PyCryptodome ECC + AES) | Encrypt Time: {enc_time:.3f} µs | Decrypt Time: {dec_time:.3f} µs")

elif choice == "3":
    enc_result, enc_time = measure_time(ecc_scalar_multiplication, 1234, 5678)
    dec_result, dec_time = measure_time(ecc_scalar_multiplication, 5678, 1234)
    print(f"[13] ECC Scalar Multiplication | Encrypt Time: {enc_time:.3f} µs | Decrypt Time: {dec_time:.3f} µs")

elif choice == "4":
    aes_key = os.urandom(32)  # Generate AES key
    enc_result, enc_time = measure_time(aes_encrypt, data, aes_key)
    dec_result, dec_time = measure_time(aes_decrypt, enc_result)
    print(f"[Ours] C_sym (AES only) | Encrypt Time: {enc_time:.3f} µs | Decrypt Time: {dec_time:.3f} µs")
else:
    print("Invalid choice. Please run the script again.")
