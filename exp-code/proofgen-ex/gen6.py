import os
import time
import random
import hashlib
from secrets import token_hex

# Path to customer data folder
customer_data_path = r"C:\Users\WINDOWS\Documents\CSS400_GDPR-RBC\cust-info"

# Simulated Quantum Key Distribution (QKD)
def simulate_qkd():
    return token_hex(32)

# Simulated Key Agreement (QKA)
def key_agreement(qkd_key, data):
    return hashlib.sha256((qkd_key + data).encode()).hexdigest()

# Generate Final Proof (Hash of QKA Key)
def generate_proof(qka_key):
    return hashlib.sha256(qka_key.encode()).hexdigest()

# Verify Proof
def verify_proof(qka_key, proof):
    return generate_proof(qka_key) == proof

# Read customer data and concatenate relevant fields
def read_customer_data(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return ''.join([line.split(': ')[1].strip() for line in content.strip().split('\n')])

# Batch Proof Generation with Random Selection
def generate_random_proof_batch(num_proofs):
    # Select random customer files
    customer_files = [f for f in os.listdir(customer_data_path) if f.endswith('.txt')]
    selected_files = random.sample(customer_files, min(num_proofs, len(customer_files)))

    total_start = time.perf_counter()

    for file_name in selected_files:
        file_path = os.path.join(customer_data_path, file_name)
        customer_data = read_customer_data(file_path)

        # Step 1: Simulate QKD
        qkd_key = simulate_qkd()

        # Step 2: Perform Key Agreement
        qka_key = key_agreement(qkd_key, customer_data)

        # Step 3: Generate Final Proof
        proof = generate_proof(qka_key)

        # Step 4: Verify Proof
        is_valid = verify_proof(qka_key, proof)
        customer_id = file_name.split('_')[1].split('.')[0]
        print(f"Customer {customer_id}: Proof Verified - {is_valid}")

    total_time = time.perf_counter() - total_start
    print(f"\nTotal Proof Generation Time for {len(selected_files)} Random Customers: {total_time:.6f} seconds")

# Execute batch proof generation
if __name__ == "__main__":
    num_proofs = 2000
    generate_random_proof_batch(num_proofs)
