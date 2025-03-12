import os
import time
import random
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Path to customer data folder
customer_data_path = r"C:\Users\WINDOWS\Documents\CSS400_GDPR-RBC\cust-info"

# Generate RSA Key Pair
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Generate RSA Proof (Signature)
def generate_rsa_proof(private_key, data):
    key = RSA.import_key(private_key)
    h = SHA256.new(data.encode())
    signature = pkcs1_15.new(key).sign(h)
    return signature

# Verify RSA Proof (Signature)
def verify_rsa_proof(public_key, data, signature):
    key = RSA.import_key(public_key)
    h = SHA256.new(data.encode())
    try:
        pkcs1_15.new(key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False

# Read customer data and concatenate relevant fields
def read_customer_data(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return ''.join([line.split(': ')[1].strip() for line in content.strip().split('\n')])

# Batch Proof Generation with Random Selection
def generate_random_proof_batch(num_proofs):
    private_key, public_key = generate_rsa_keys()

    # Randomly select customer files
    customer_files = [f for f in os.listdir(customer_data_path) if f.endswith('.txt')]
    selected_files = random.sample(customer_files, min(num_proofs, len(customer_files)))

    total_start = time.perf_counter()

    for file_name in selected_files:
        file_path = os.path.join(customer_data_path, file_name)
        customer_data = read_customer_data(file_path)

        # Generate Proof
        proof = generate_rsa_proof(private_key, customer_data)

        # Verify Proof
        is_valid = verify_rsa_proof(public_key, customer_data, proof)
        customer_id = file_name.split('_')[1].split('.')[0]
        print(f"Customer {customer_id}: Proof Verified - {is_valid}")

    total_time = time.perf_counter() - total_start
    print(f"\nTotal Proof Generation Time for {len(selected_files)} Random Customers: {total_time:.6f} seconds")

# Execute random proof generation
if __name__ == "__main__":
    num_proofs = 2000
    generate_random_proof_batch(num_proofs)
