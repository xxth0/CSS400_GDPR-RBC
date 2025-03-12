import time
import json
import os
from web3 import Web3
from dotenv import load_dotenv
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from charm.toolbox.pairinggroup import PairingGroup, GT
from charm.schemes.abenc.abenc_cpabe import CPabe

# Load environment variables from .env file
load_dotenv()

# Blockchain configuration from .env
ganache_url = os.getenv("GANACHE_URL")
private_key = os.getenv("PRIVATE_KEY")
contract_address = os.getenv("CONTRACT_ADDRESS")
contract_json_path = os.getenv("CONTRACT_JSON_PATH")

# Load contract details
with open(contract_json_path) as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider(ganache_url))
account = web3.eth.account.from_key(private_key)

# Connect to the contract
contract = web3.eth.contract(address=contract_address, abi=abi)

# Initialize CP-ABE
group = PairingGroup('SS512')
cpabe = CPabe(group)
master_public_key, master_secret_key = cpabe.setup()

# CP-ABE Key Generation for specific attributes
def generate_user_key(attributes):
    return cpabe.keygen(master_public_key, master_secret_key, attributes)

# CP-ABE Encryption of AES key with policy
def encrypt_key(aes_key, policy):
    return cpabe.encrypt(master_public_key, aes_key, policy)

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
def redact_customers_batch(start_id, end_id, original_data, redacted_data, policy):
    total_start = time.perf_counter()

    for customer_id in range(start_id, end_id + 1):
        # Generate AES Key
        aes_key = generate_key()

        # Encrypt Data with AES
        encrypted_original = encrypt_data(aes_key, original_data)
        encrypted_redacted = encrypt_data(aes_key, redacted_data)

        # Encrypt AES Key using CP-ABE
        encrypted_aes_key = encrypt_key(aes_key, policy)

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

# Define the access policy (example)
access_policy = '((role:manager AND department:finance) OR role:admin)'

# Perform batch redaction from customer ID 3001 to 4000
redact_customers_batch(3001, 4000, original_data, redacted_data, access_policy)
