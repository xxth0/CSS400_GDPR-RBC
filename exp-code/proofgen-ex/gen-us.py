import os
import time
import hashlib
import random
from secrets import token_hex

# Path to customer data folder
customer_data_path = r"C:\Users\WINDOWS\Documents\CSS400_GDPR-RBC\cust-info"

# Generate Individual Proof (Simulated ZKP)
def generate_individual_proof(data):
    return hashlib.sha256(data.encode()).digest()

# Aggregate Proofs for Batch (Roll-Up)
def aggregate_proofs(proofs):
    combined = b''.join(proofs)
    return hashlib.sha256(combined).digest()

# Verify the Batch Proof (Simple Verification by Re-Aggregation)
def verify_batch_proof(proofs, batch_proof):
    expected_proof = aggregate_proofs(proofs)
    return expected_proof == batch_proof

# Read customer data and concatenate relevant fields
def read_customer_data(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return ''.join([line.split(': ')[1].strip() for line in content.strip().split('\n')])

# Batch Proof Generation with Specific Number of Proofs
def generate_batch_proof(num_proofs, batch_size=100):
    customer_files = [f for f in os.listdir(customer_data_path) if f.endswith('.txt')]
    random.shuffle(customer_files)

    # Select only the number of proofs required
    selected_files = customer_files[:num_proofs]

    total_start = time.perf_counter()

    batch_index = 0
    for i in range(0, len(selected_files), batch_size):
        batch_files = selected_files[i:i + batch_size]

        # Generate Individual Proofs for the Batch
        individual_proofs = []
        for file_name in batch_files:
            file_path = os.path.join(customer_data_path, file_name)
            customer_data = read_customer_data(file_path)

            # Generate individual proof
            proof = generate_individual_proof(customer_data)
            individual_proofs.append(proof)

        # Aggregate Proofs (Roll-up)
        batch_proof = aggregate_proofs(individual_proofs)

        # Verify the Batch Proof
        is_valid = verify_batch_proof(individual_proofs, batch_proof)
        print(f"Batch {batch_index + 1}: Proof Verified - {is_valid}")

        batch_index += 1

    total_time = time.perf_counter() - total_start
    print(f"\nTotal Proof Generation Time for {num_proofs} Proofs (Batch Size {batch_size}): {total_time:.6f} seconds")

# Execute batch proof generation
if __name__ == "__main__":
    num_proofs = 250
    generate_batch_proof(num_proofs)
