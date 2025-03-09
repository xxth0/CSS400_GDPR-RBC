from web3 import Web3
import json
import os
import random

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Load contract details
contract_json_path = r"C:\Users\WINDOWS\Documents\CSS400_GDPR-RBC\build\contracts\CustomerStorageFull.json"

with open(contract_json_path) as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]
    contract_address = "0x06DF2c7C90bAe86e9f4D26BA8632242f04087DbF"  # Ensure this is correct

contract = web3.eth.contract(address=contract_address, abi=abi)

# Get the first account from Ganache
account = web3.eth.accounts[0]

# Path to customer data files
customer_files_dir = r"C:\Users\WINDOWS\Documents\CSS400_GDPR-RBC\cust-info"
trapdoor_file = "trapdoor_keys.json"
customer_data_file = "customer_data.json"

# Load existing trapdoor keys if available
if os.path.exists(trapdoor_file):
    with open(trapdoor_file, "r") as f:
        trapdoor_keys = json.load(f)
else:
    trapdoor_keys = {}

# Load existing plain text customer data if available
if os.path.exists(customer_data_file):
    with open(customer_data_file, "r") as f:
        customer_data = json.load(f)
else:
    customer_data = {}

# Chameleon Hash Function
def chameleon_hash(message, trapdoor_key=None):
    """Generate a Chameleon Hash with a trapdoor key."""
    if trapdoor_key is None:
        trapdoor_key = random.randint(1, 2**256)  # Generate a random trapdoor key
    
    # Compute the Chameleon Hash (message XOR trapdoor_key mod large prime)
    large_prime = 2**256 - 429  # A large prime number
    message_int = int.from_bytes(Web3.keccak(text=message), byteorder="big")
    hash_value = (message_int ^ trapdoor_key) % large_prime

    return hash_value, trapdoor_key

# Process customer files (only first 10 for testing)
for i in range(1, 11):
    file_path = os.path.join(customer_files_dir, f"customer_{i}.txt")

    # Check if file exists before processing
    if not os.path.exists(file_path):
        print(f"Skipping missing file: {file_path}")
        continue

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.read().strip().split("\n")

            if len(lines) < 5:
                print(f"Skipping invalid file (insufficient data): {file_path}")
                continue

            customer = {
                "nat_id": lines[0].strip(),
                "consent": lines[1].strip(),
                "CID": lines[2].strip(),
                "hFIID": lines[3].strip(),
                "sigFIID": lines[4].strip(),
                "is_redacted": False  # Default: not redacted
            }

            # Store plain text customer data in JSON
            customer_data[i] = customer  

            # Generate Chameleon Hashes and Trapdoor Keys
            chameleon_hash_value, trapdoor_nat = chameleon_hash(customer["nat_id"])
            enc_nat_id = Web3.to_bytes(chameleon_hash_value)

            chameleon_hash_value, trapdoor_consent = chameleon_hash(customer["consent"])
            enc_consent = Web3.to_bytes(chameleon_hash_value)

            chameleon_hash_value, trapdoor_CID = chameleon_hash(customer["CID"])
            enc_CID = Web3.to_bytes(chameleon_hash_value)

            chameleon_hash_value, trapdoor_h_FI_ID = chameleon_hash(customer["hFIID"])
            enc_h_FI_ID = Web3.to_bytes(chameleon_hash_value)

            chameleon_hash_value, trapdoor_sig_FI_ID = chameleon_hash(customer["sigFIID"])
            enc_sig_FI_ID = Web3.to_bytes(chameleon_hash_value)

            # Store trapdoor keys for redaction
            trapdoor_keys[i] = {
                "nat_id": trapdoor_nat,
                "consent": trapdoor_consent,
                "CID": trapdoor_CID,
                "hFIID": trapdoor_h_FI_ID,
                "sigFIID": trapdoor_sig_FI_ID
            }

            # Fix: Add the missing argument (chameleon hash)
            chameleon_hash_final, trapdoor_final = chameleon_hash("final_hash_value")
            chameleon_hash_final_bytes = Web3.to_bytes(chameleon_hash_final)

            # Send transaction to blockchain
            tx = contract.functions.addCustomer(
                chameleon_hash_final_bytes,  # Fixed: Add this missing argument
                enc_nat_id,
                enc_consent,
                enc_CID,
                enc_h_FI_ID,
                enc_sig_FI_ID
            ).transact({"from": account})

            # Wait for confirmation
            receipt = web3.eth.wait_for_transaction_receipt(tx)
            print(f"Customer {i} added successfully: {receipt.transactionHash.hex()}")

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

# Save trapdoor keys for future redaction
with open(trapdoor_file, "w") as f:
    json.dump(trapdoor_keys, f, indent=4)

# Save plain text customer data
with open(customer_data_file, "w") as f:
    json.dump(customer_data, f, indent=4)

print("Trapdoor keys and customer data saved.")
