from web3 import Web3
import json
import os

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

# Fetch customer details (Modify customer index as needed)
customer_index = 5  # Change this index to retrieve other customers

try:
    customer_data = contract.functions.getCustomer(customer_index).call()
except Exception as e:
    print(f"Error retrieving customer data: {e}")
    exit()

# Extract stored Chameleon Hash values
chameleon_hash = customer_data[0].hex()
encrypted_nat_id = customer_data[1].hex()
encrypted_consent = customer_data[2].hex()
encrypted_CID = customer_data[3].hex()
encrypted_h_FI_ID = customer_data[4].hex()
encrypted_sig_FI_ID = customer_data[5].hex()
uploader = customer_data[6]

# Print Retrieved Data
print("\n--- Retrieved Data ---")
print(f"Customer Number: {customer_index+1}")
print(f"Chameleon Hash (Main): {chameleon_hash}")

print("\nStored Hash Values from Blockchain:")
print(f"Hash of NatID: {encrypted_nat_id}")
print(f"Hash of Consent: {encrypted_consent}")
print(f"Hash of CID: {encrypted_CID}")
print(f"Hash of h_FI_ID: {encrypted_h_FI_ID}")
print(f"Hash of sig_FI_ID: {encrypted_sig_FI_ID}")
print(f"Uploader Address: {uploader}")
