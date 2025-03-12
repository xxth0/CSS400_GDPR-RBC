import time
import json
import random
import hashlib
from web3 import Web3
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Blockchain Configuration
ganache_url = os.getenv("GANACHE_URL")
private_key = os.getenv("PRIVATE_KEY")
contract_address = os.getenv("CONTRACT_ADDRESS")
contract_json_path = os.getenv("CONTRACT_JSON_PATH")

# Load contract details
with open(contract_json_path) as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]

# Connect to Ganache and the contract
web3 = Web3(Web3.HTTPProvider(ganache_url))
account = web3.eth.account.from_key(private_key)
contract = web3.eth.contract(address=contract_address, abi=abi)

# Batch sending function
def send_batch(transactions):
    for tx in transactions:
        try:
            tx_hash = web3.eth.send_raw_transaction(tx)
            print(f"Transaction sent: {tx_hash.hex()}")
        except Exception as e:
            print(f"Transaction failed: {e}")

# Batch redaction with nonce management
def redact_customers_in_batches(start_id, end_id, batch_size=100):
    total_start = time.perf_counter()
    current_nonce = web3.eth.get_transaction_count(account.address)
    transactions = []

    for i, customer_id in enumerate(range(start_id, end_id + 1)):
        # Build the redaction transaction
        tx = contract.functions.redactCustomer(customer_id).build_transaction({
            'from': account.address,
            'nonce': current_nonce,
            'gas': 200000,
            'maxFeePerGas': web3.to_wei('2', 'gwei'),
            'maxPriorityFeePerGas': web3.to_wei('1', 'gwei')
        })
        
        # Sign the transaction
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        transactions.append(signed_tx.raw_transaction)
        current_nonce += 1

        # Send batch if full or it's the last transaction
        if len(transactions) == batch_size or customer_id == end_id:
            print(f"\nSending batch of {len(transactions)} transactions...")
            send_batch(transactions)
            transactions.clear()

    total_time = time.perf_counter() - total_start
    print(f"\nTotal redaction time for customers {start_id}-{end_id}: {total_time:.6f} seconds")

# Run the batch redaction
redact_customers_in_batches(1001, 2000, batch_size=100)
