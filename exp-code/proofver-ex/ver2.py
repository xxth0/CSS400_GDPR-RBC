import json
import os
import time
from web3 import Web3
from dotenv import load_dotenv
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

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

# Store Proof On-Chain with Higher Gas Limit
def store_proof_on_chain(customer_id, proof):
    tx = contract.functions.storeProof(customer_id, proof.hex()).transact({
        "from": account.address,
        "gas": 1000000,   # Increase gas limit to 1,000,000
        "maxFeePerGas": web3.to_wei('2', 'gwei'), 
        "maxPriorityFeePerGas": web3.to_wei('1', 'gwei') 
    })
    web3.eth.wait_for_transaction_receipt(tx)

# Retrieve Proof from Blockchain
def retrieve_proof(customer_id):
    return bytes.fromhex(contract.functions.getProof(customer_id).call())

# Process Customers and Calculate Total Time
def process_customers(start_id, end_id):
    private_key, public_key = generate_rsa_keys()
    data = "Sensitive Customer Data"

    total_start = time.perf_counter()

    for customer_id in range(start_id, end_id + 1):
        proof = generate_rsa_proof(private_key, data)
        store_proof_on_chain(customer_id, proof)

        retrieved_proof = retrieve_proof(customer_id)
        is_valid = verify_rsa_proof(public_key, data, retrieved_proof)

        print(f"Customer {customer_id}: Proof Verified - {is_valid}")

    total_time = time.perf_counter() - total_start
    print(f"\nTotal Time Spent for Customers {start_id}-{end_id}: {total_time:.6f} seconds")

# Example Usage
if __name__ == "__main__":
    process_customers(1, 2000)
