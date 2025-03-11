import time
import json
import random
from web3 import Web3
import hashlib

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

# Multiplicative Hash Function
def generate_key():
    return random.randint(1, 2**256)

def multiplicative_hash(data, key):
    combined = (data + str(key)).encode()
    return hashlib.sha256(combined).hexdigest()

# Redact customers and calculate total time
def redact_customers_batch(start_id, end_id, original_data, redacted_data):
    total_start = time.perf_counter()

    for customer_id in range(start_id, end_id + 1):
        key = generate_key()
        original_hash = multiplicative_hash(original_data, key)
        redacted_hash = multiplicative_hash(redacted_data, key)

        # Blockchain transaction
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
original_data = "Original Sensitive Data Multiplicative"
redacted_data = "REDACTED Multiplicative"

# Perform batch redaction from customer ID 21 to 30
redact_customers_batch(201, 300, original_data, redacted_data)
