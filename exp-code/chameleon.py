from web3 import Web3
import json
import os
import time
import hashlib
import random

# Connect to blockchain (Ganache)
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Load contract details (Redactable Storage)
contract_json_path = r"C:\\Users\\WINDOWS\\Documents\\CSS400_GDPR-RBC\\build\\contracts\\CustomerStorageFull.json"

with open(contract_json_path) as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]
    contract_address = "0xFfBDD4dCBEAdc64A7f749C52352CE4A7CEB40dF9"

contract = web3.eth.contract(address=contract_address, abi=abi)

# Load customer data JSON
customer_data_file = "customer_data.json"
trapdoor_file = "trapdoor_keys.json"

if os.path.exists(customer_data_file):
    with open(customer_data_file, "r") as f:
        customer_data = json.load(f)
else:
    customer_data = {}

if os.path.exists(trapdoor_file):
    with open(trapdoor_file, "r") as f:
        trapdoor_keys = json.load(f)
else:
    trapdoor_keys = {}

customer_to_remove = "5"
account = web3.eth.accounts[0]

customer_count = contract.functions.customerCount().call()
print(f"Total customers stored on-chain: {customer_count}")

if int(customer_to_remove) >= customer_count:
    print(f"❌ Customer {customer_to_remove} does not exist. Aborting.")
else:
    customer_info = contract.functions.getCustomer(int(customer_to_remove)).call()
    is_redacted = customer_info[7]

    if is_redacted:
        print(f"⚠️ Customer {customer_to_remove} is already redacted. Skipping.")
    else:
        try:
            old_hash = customer_info[6]
            print(f"Old Hash: {old_hash}")

            start_time = time.time()
            new_random = random.randint(0, 1_000_000)
            new_hash_input = f"{customer_info[1]}_{new_random}".encode()
            new_hash = hashlib.sha256(new_hash_input).hexdigest()
            end_time = time.time()

            print(f"New Random Number: {new_random}")
            print(f"New Hash: {new_hash}")
            print(f"Time spent recalculating hash: {end_time - start_time:.6f} seconds")

            tx = contract.functions.redactCustomer(int(customer_to_remove)).transact({"from": account})
            receipt = web3.eth.wait_for_transaction_receipt(tx)
            print(f"✅ Redacted Customer {customer_to_remove}: {receipt.transactionHash.hex()}")

            if customer_to_remove in customer_data:
                del customer_data[customer_to_remove]

            if customer_to_remove in trapdoor_keys:
                del trapdoor_keys[customer_to_remove]

            with open(customer_data_file, "w") as f:
                json.dump(customer_data, f, indent=4)

            with open(trapdoor_file, "w") as f:
                json.dump(trapdoor_keys, f, indent=4)

            print(f"✅ Customer {customer_to_remove} successfully redacted and trapdoor key deleted.")

        except Exception as e:
            print(f"❌ Error redacting Customer {customer_to_remove}: {str(e)}")
