import json
import os
import time
import hashlib
import secrets
import base64
from web3 import Web3
from dotenv import load_dotenv

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

# Simulated Quantum Key Distribution (QKD)
def simulate_qkd():
    return secrets.token_hex(32)

# Simulated Key Agreement (QKA)
def key_agreement(qkd_key, data):
    return hashlib.sha256((qkd_key + data).encode()).digest()

# Generate Final Proof
def generate_proof(qka_key):
    return hashlib.sha256(qka_key).digest()

# Store Proof On-Chain (Compressed)
def store_proof_on_chain(customer_id, proof):
    compressed_proof = base64.b64encode(proof).decode()
    tx = contract.functions.storeProof(customer_id, compressed_proof).transact({
        "from": account.address,
        "gas": 1000000,
        "maxFeePerGas": web3.to_wei('2', 'gwei'),
        "maxPriorityFeePerGas": web3.to_wei('1', 'gwei')
    })
    web3.eth.wait_for_transaction_receipt(tx)

# Retrieve and Decode Proof from Blockchain
def retrieve_proof(customer_id):
    compressed_proof = contract.functions.getProof(customer_id).call()
    return base64.b64decode(compressed_proof)

# Verify the Proof
def verify_proof(qka_key, stored_proof):
    expected_proof = generate_proof(qka_key)
    return expected_proof == stored_proof

# Process Customers and Calculate Total Time
def process_customers(start_id, end_id):
    data = "Sensitive Customer Data"

    total_start = time.perf_counter()

    for customer_id in range(start_id, end_id + 1):
        # Proof Generation (QKD + QKA + Final Proof)
        qkd_key = simulate_qkd()
        qka_key = key_agreement(qkd_key, data)
        proof = generate_proof(qka_key)

        # Store Proof on Blockchain
        store_proof_on_chain(customer_id, proof)

        # Retrieve and Verify Proof
        retrieved_proof = retrieve_proof(customer_id)
        is_valid = verify_proof(qka_key, retrieved_proof)

        print(f"Customer {customer_id}: Proof Verified - {is_valid}")

    total_time = time.perf_counter() - total_start
    print(f"\nTotal Time Spent for Customers {start_id}-{end_id}: {total_time:.6f} seconds")

# Run Batch Processing
if __name__ == "__main__":
    process_customers(1, 2000)
