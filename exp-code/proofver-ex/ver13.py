import json
import os
import time
from web3 import Web3
from dotenv import load_dotenv
from ecdsa import SigningKey, SECP256k1, VerifyingKey, BadSignatureError

# Load environment variables
load_dotenv()

# Load configuration from .env
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

# Generate ECC Proof
def generate_ecc_proof(data):
    private_key = SigningKey.generate(curve=SECP256k1)
    signature = private_key.sign(data.encode())
    return signature, private_key.verifying_key

# Store Proof On-Chain
def store_proof_on_chain(customer_id, proof):
    tx = contract.functions.storeProof(customer_id, proof.hex()).transact({
        "from": account.address,
        "gas": 300000
    })
    web3.eth.wait_for_transaction_receipt(tx)
    print(f"Proof stored for customer {customer_id}. Transaction: {tx.hex()}")

# Retrieve Proof from Blockchain
def retrieve_proof(customer_id):
    return bytes.fromhex(contract.functions.getProof(customer_id).call())

# Verify ECC Proof with timing
def verify_ecc_proof(public_key, data, proof):
    start_time = time.perf_counter()
    try:
        is_valid = public_key.verify(proof, data.encode())
    except BadSignatureError:
        is_valid = False
    end_time = time.perf_counter()
    verification_time = end_time - start_time
    return is_valid, verification_time

# Batch Processing for Range of Customers
def process_customers(start_id, end_id):
    data = "Sensitive Customer Data"
    total_verification_time = 0

    for customer_id in range(start_id, end_id + 1):
        # Generate and Store Proof
        proof, pub_key = generate_ecc_proof(data)
        store_proof_on_chain(customer_id, proof)

        # Retrieve and Verify Proof
        retrieved_proof = retrieve_proof(customer_id)
        is_valid, verification_time = verify_ecc_proof(pub_key, data, retrieved_proof)

        print(f"Customer {customer_id}: Proof Verified - {is_valid} | Verification Time: {verification_time:.6f} seconds")
        total_verification_time += verification_time

    print(f"\nTotal Verification Time for Customers {start_id}-{end_id}: {total_verification_time:.6f} seconds")

# Run batch processing for a given range
if __name__ == "__main__":
    # Example ranges
    process_customers(1, 2000)

