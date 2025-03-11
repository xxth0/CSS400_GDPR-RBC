import time
import json
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
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

# ECC Functions
def ecc_generate_keys():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    return private_key, public_key

def ecc_sign_data(private_key, data):
    return private_key.sign(data.encode(), ec.ECDSA(hashes.SHA256()))

# Redact customers and calculate total time
def redact_customers_batch(start_id, end_id, original_data, redacted_data):
    total_start = time.perf_counter()

    for customer_id in range(start_id, end_id + 1):
        private_key, public_key = ecc_generate_keys()
        original_signature = ecc_sign_data(private_key, original_data)
        redacted_signature = ecc_sign_data(private_key, redacted_data)

        # Blockchain Update
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
original_data = "Original Sensitive Data ECC"
redacted_data = "REDACTED ECC"

# Perform batch redaction from customer ID 31 to 40
redact_customers_batch(101, 200, original_data, redacted_data)
