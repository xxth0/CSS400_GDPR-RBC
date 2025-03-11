import time
import json
import os
from web3 import Web3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Blockchain connection details
ganache_url = "http://127.0.0.1:7545"
private_key = "0x37a47e900a171b86983dcf1f15fbbbf580fed1776a97297cefff6cd8ddccade1"

# Load contract details
contract_json_path = r"C:\\Users\\WINDOWS\\Documents\\CSS400_GDPR-RBC\\build\\contracts\\CustomerStorageFull.json"
with open(contract_json_path) as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]
    contract_address = "0x25B08c964D49F759704F6d312e4657707B03eb77"

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider(ganache_url))
account = web3.eth.account.from_key(private_key)

# Connect to the contract
contract = web3.eth.contract(address=contract_address, abi=abi)

# AES Encryption Functions
def generate_key():
    return os.urandom(32)

def encrypt_data(key, plaintext):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padded_plaintext = plaintext.ljust(32).encode()  # Simple padding
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return iv + ciphertext

# Redact customers and calculate total time
def redact_customers_batch(start_id, end_id, original_data, redacted_data):
    total_start = time.perf_counter()

    for customer_id in range(start_id, end_id + 1):
        key = generate_key()
        encrypted_original = encrypt_data(key, original_data)
        encrypted_redacted = encrypt_data(key, redacted_data)

        # Blockchain transaction (using encrypted redacted data)
        tx = contract.functions.redactCustomer(customer_id).transact({
            "from": account.address,
            "gas": 300000,
            "maxFeePerGas": web3.to_wei('2', 'gwei'),
            "maxPriorityFeePerGas": web3.to_wei('1', 'gwei')
        })

        print(f"Customer {customer_id} redacted. Transaction hash: {tx.hex()}")

    total_time = time.perf_counter() - total_start
    print(f"\nTotal redaction time for customers {start_id}-{end_id}: {total_time:.6f} seconds")

# Parameters for batch redaction
original_data = "Original Sensitive Data ABE"
redacted_data = "REDACTED ABE"

# Perform batch redaction from customer ID 71 to 80
redact_customers_batch(301, 400, original_data, redacted_data)
