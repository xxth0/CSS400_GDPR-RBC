import os
import time
import random
from hashlib import sha256
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature, encode_dss_signature
from cryptography.exceptions import InvalidSignature

# Path to customer data folder
customer_data_path = r"C:\Users\WINDOWS\Documents\CSS400_GDPR-RBC\cust-info"

# Generate ECC Key Pair
def generate_ecc_keys():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    return private_key, public_key

# Generate ECC Proof (Signature)
def generate_ecc_proof(private_key, data):
    signature = private_key.sign(data.encode(), ec.ECDSA(hashes.SHA256()))
    return signature

# Verify ECC Proof
def verify_ecc_proof(public_key, data, signature):
    try:
        public_key.verify(signature, data.encode(), ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False

# Hashing with Modular Addition
def hash_with_mod_add(data):
    return int(sha256(data.encode()).hexdigest(), 16) % (2**256)

# Read customer data and concatenate relevant fields
def read_customer_data(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return ''.join([line.split(': ')[1].strip() for line in content.strip().split('\n')])

# Batch Proof Generation with Random Selection
def generate_random_proof_batch(num_proofs):
    private_key, public_key = generate_ecc_keys()

    # Randomly select customer files
    customer_files = [f for f in os.listdir(customer_data_path) if f.endswith('.txt')]
    selected_files = random.sample(customer_files, min(num_proofs, len(customer_files)))

    total_start = time.perf_counter()

    for file_name in selected_files:
        file_path = os.path.join(customer_data_path, file_name)
        customer_data = read_customer_data(file_path)

        # Step 1: Generate ECC Signature
        signature = generate_ecc_proof(private_key, customer_data)

        # Step 2: Perform Hash with Modular Addition
        hashed_value = hash_with_mod_add(customer_data)

        # Step 3: Verify ECC Proof
        is_valid = verify_ecc_proof(public_key, customer_data, signature)
        customer_id = file_name.split('_')[1].split('.')[0]
        print(f"Customer {customer_id}: Proof Verified - {is_valid}")

    total_time = time.perf_counter() - total_start
    print(f"\nTotal Proof Generation Time for {len(selected_files)} Random Customers: {total_time:.6f} seconds")

# Execute batch proof generation
if __name__ == "__main__":
    num_proofs = 2000
    generate_random_proof_batch(num_proofs)
