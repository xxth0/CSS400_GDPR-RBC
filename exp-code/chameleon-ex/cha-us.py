import time
import json
import random
import hashlib
from web3 import Web3

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

# Chameleon Hash Functions
def generate_trapdoor():
    return random.randint(1, 2**256)

def chameleon_hash(data, trapdoor):
    prime = 2**256 - 429
    data_int = int.from_bytes(hashlib.sha256(data.encode()).digest(), byteorder="big")
    return (data_int ^ trapdoor) % prime

def create_collision(original_int, redacted_data, trapdoor):
    redacted_int = int.from_bytes(hashlib.sha256(redacted_data.encode()).digest(), byteorder="big")
    return (original_int ^ trapdoor) ^ redacted_int

# Redact customers and calculate total time
def redact_customers_batch(start_id, end_id, original_data, redacted_data):
    total_start = time.perf_counter()

    for customer_id in range(start_id, end_id + 1):
        trapdoor = generate_trapdoor()
        original_int = int.from_bytes(hashlib.sha256(original_data.encode()).digest(), byteorder="big")
        new_trapdoor = create_collision(original_int, redacted_data, trapdoor)
        new_hash = chameleon_hash(redacted_data, new_trapdoor)

        tx = contract.functions.redactCustomer(customer_id).transact({
            "from": account.address,
            "gas": 200000,
            "maxFeePerGas": web3.to_wei('2', 'gwei'),
            "maxPriorityFeePerGas": web3.to_wei('1', 'gwei')
        })

        print(f"Customer {customer_id} redacted. Transaction hash: {tx.hex()}")

    total_time = time.perf_counter() - total_start
    print(f"\nTotal redaction time for customers {start_id}-{end_id}: {total_time:.6f} seconds")

# Parameters for batch redaction
original_data = "Original Sensitive Data"
redacted_data = "REDACTED"

# Perform batch redaction from customer ID 11 to 20
redact_customers_batch(1, 100, original_data, redacted_data)
