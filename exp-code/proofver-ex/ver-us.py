import json
import os
import time
import hashlib
import base64
from web3 import Web3
from dotenv import load_dotenv
from secrets import token_hex

# Load environment variables
load_dotenv()

# Blockchain configuration from .env
ganache_url = os.getenv("GANACHE_URL")
private_key = os.getenv("PRIVATE_KEY")
contract_address = os.getenv("CONTRACT_ADDRESS")
contract_json_path = os.getenv("CONTRACT_JSON_PATH")

# Load contract details
with open(contract_json_path) as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]

# Connect to Ganache and Contract
web3 = Web3(Web3.HTTPProvider(ganache_url))
account = web3.eth.account.from_key(private_key)
contract = web3.eth.contract(address=contract_address, abi=abi)

# Generate Individual Proof (Simulated ZKP)
def generate_individual_proof(data):
    return hashlib.sha256(data.encode()).digest()

# Aggregate and Compress Proofs for Roll-Up
def aggregate_proofs(proofs):
    combined = b''.join(proofs)
    return hashlib.sha256(combined).digest()

# Store Batch Proof On-Chain (Compressed)
def store_batch_proof_on_chain(batch_id, proof):
    compressed_proof = base64.b64encode(proof).decode()
    tx = contract.functions.storeProof(batch_id, compressed_proof).transact({
        "from": account.address,
        "gas": 2000000,
        "maxFeePerGas": web3.to_wei('2', 'gwei'),
        "maxPriorityFeePerGas": web3.to_wei('1', 'gwei')
    })
    web3.eth.wait_for_transaction_receipt(tx)

# Retrieve and Decode Batch Proof from Blockchain
def retrieve_batch_proof(batch_id):
    compressed_proof = contract.functions.getProof(batch_id).call()
    return base64.b64decode(compressed_proof)

# Verify Batch Proof (Simulated)
def verify_batch_proof(proofs, stored_proof):
    expected_proof = aggregate_proofs(proofs)
    return expected_proof == stored_proof

# Process Customers in Batches with Total Timing
def process_customer_batches(start_id, end_id, batch_size):
    data = "Sensitive Customer Data"
    total_start = time.perf_counter()
    batch_id = 0

    for i in range(start_id, end_id + 1, batch_size):
        batch_proofs = []

        for customer_id in range(i, min(i + batch_size, end_id + 1)):
            proof = generate_individual_proof(data + str(customer_id))
            batch_proofs.append(proof)

        aggregated_proof = aggregate_proofs(batch_proofs)
        store_batch_proof_on_chain(batch_id, aggregated_proof)

        # Retrieve and Verify
        stored_proof = retrieve_batch_proof(batch_id)
        is_valid = verify_batch_proof(batch_proofs, stored_proof)

        print(f"Batch {batch_id}: Proof Verified - {is_valid}")
        batch_id += 1

    total_time = time.perf_counter() - total_start
    print(f"\nTotal Time Spent for Customers {start_id}-{end_id}: {total_time:.6f} seconds")

# Run Batch Processing for Large Ranges
if __name__ == "__main__":
    process_customer_batches(1, 2000, 100)   # Batch of 100 customers