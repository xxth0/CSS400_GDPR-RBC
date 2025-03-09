from web3 import Web3
import json
import os

# Connect to blockchain (Ganache)
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Load contract details (Redactable Storage)
contract_json_path = r"C:\Users\WINDOWS\Documents\CSS400_GDPR-RBC\build\contracts\CustomerStorageFull.json"

with open(contract_json_path) as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]
    contract_address = "0x06DF2c7C90bAe86e9f4D26BA8632242f04087DbF"  # Ensure this is correct

contract = web3.eth.contract(address=contract_address, abi=abi)

# Load customer data JSON
customer_data_file = "customer_data.json"
trapdoor_file = "trapdoor_keys.json"

# Load stored customer data
if os.path.exists(customer_data_file):
    with open(customer_data_file, "r") as f:
        customer_data = json.load(f)
else:
    customer_data = {}

# Load stored trapdoor keys
if os.path.exists(trapdoor_file):
    with open(trapdoor_file, "r") as f:
        trapdoor_keys = json.load(f)
else:
    trapdoor_keys = {}

# Set the customer index you want to redact
customer_to_remove = "5"  # Change this if needed

# Get account for transaction
account = web3.eth.accounts[0]

# Debug: Check total customers stored
customer_count = contract.functions.customerCount().call()
print(f"Total customers stored on-chain: {customer_count}")

# Validate customer index
if int(customer_to_remove) >= customer_count:
    print(f"❌ Customer {customer_to_remove} does not exist. Aborting.")
else:
    # Debug: Check if customer is already redacted
    customer_info = contract.functions.getCustomer(int(customer_to_remove)).call()
    is_redacted = customer_info[7]  # `isRedacted` is the last value returned

    if is_redacted:
        print(f"⚠️ Customer {customer_to_remove} is already redacted. Skipping.")
    else:
        try:
            # Send redaction transaction to the smart contract
            tx = contract.functions.redactCustomer(int(customer_to_remove)).transact({"from": account})
            receipt = web3.eth.wait_for_transaction_receipt(tx)
            print(f"✅ Redacted Customer {customer_to_remove}: {receipt.transactionHash.hex()}")

            # Remove customer data completely
            if customer_to_remove in customer_data:
                del customer_data[customer_to_remove]

            # Also remove trapdoor key
            if customer_to_remove in trapdoor_keys:
                del trapdoor_keys[customer_to_remove]

            # Save updated JSON without redacted entry
            with open(customer_data_file, "w") as f:
                json.dump(customer_data, f, indent=4)

            # Save updated trapdoor keys without deleted one
            with open(trapdoor_file, "w") as f:
                json.dump(trapdoor_keys, f, indent=4)

            print(f"✅ Customer {customer_to_remove} successfully redacted and trapdoor key deleted.")

        except Exception as e:
            print(f"❌ Error redacting Customer {customer_to_remove}: {str(e)}")
