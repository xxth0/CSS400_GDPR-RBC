import time
import hashlib
import random
import os
import json
from web3 import Web3
from dotenv import load_dotenv
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import pandas as pd
from web3.exceptions import ContractLogicError

# Load environment variables
load_dotenv()

GANACHE_URL = os.getenv("GANACHE_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Load contract details (Redactable Storage)
contract_json_path = r"C:\\Users\\WINDOWS\\Documents\\CSS400_GDPR-RBC\\build\\contracts\\CustomerStorageFull.json"

with open(contract_json_path) as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]
    contract_address = "0xFfBDD4dCBEAdc64A7f749C52352CE4A7CEB40dF9"

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)

# Connect to the contract
contract = web3.eth.contract(address=contract_address, abi=abi)

benchmark_results = {}

# ----------------- Helper Functions ----------------- #
def generate_trapdoor():
    return random.randint(1, 2**256)

def chameleon_hash(data, trapdoor):
    prime = 2**256 - 429
    data_int = int.from_bytes(hashlib.sha256(data.encode()).digest(), 'big')
    return (data_int ^ trapdoor) % prime

def create_collision(original_data, redacted_data, trapdoor):
    prime = 2**256 - 429
    original_int = int.from_bytes(hashlib.sha256(original_data.encode()).digest(), 'big')
    redacted_int = int.from_bytes(hashlib.sha256(redacted_data.encode()).digest(), 'big')
    return (original_int ^ trapdoor) ^ redacted_int

def ecc_generate_keys():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    return private_key, public_key

def ecc_sign_data(private_key, data):
    if isinstance(data, bytes):
        data = data.hex()
    return private_key.sign(data.encode(), ec.ECDSA(hashes.SHA256()))

def generate_symmetric_key():
    return os.urandom(32)

def encrypt_data(key, plaintext):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padded_plaintext = plaintext.ljust(32).encode()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return iv + ciphertext

# ----------------- Benchmark Each Scheme ----------------- #
for customer_id in range(2, 2):
    try:
        # Try to retrieve the customer data
        customer = contract.functions.getCustomer(customer_id).call()
        
        # Skip already redacted customers
        if customer[-1]:
            print(f"Customer {customer_id} is already redacted. Skipping...")
            continue
        
        # Prepare customer data
        customer_data = customer[0].hex() if isinstance(customer[0], bytes) else str(customer[0])

        # ----------------- ECC Scheme ----------------- #
        start = time.perf_counter()
        private_key, public_key = ecc_generate_keys()
        signature = ecc_sign_data(private_key, customer_data)
        end = time.perf_counter()
        ecc_time = end - start

        # ----------------- Multiplicative Hash ----------------- #
        start = time.perf_counter()
        key = random.randint(1, 2**256)
        hash_value = int.from_bytes(hashlib.sha256((customer_data + str(key)).encode()).digest(), 'big')
        end = time.perf_counter()
        mult_hash_time = end - start

        # ----------------- ABE (Simulated with AES) ----------------- #
        start = time.perf_counter()
        aes_key = generate_symmetric_key()
        encrypted = encrypt_data(aes_key, customer_data)
        end = time.perf_counter()
        abe_time = end - start

        # ----------------- Chameleon Hash ----------------- #
        start = time.perf_counter()
        trapdoor = generate_trapdoor()
        cham_hash = chameleon_hash(customer_data, trapdoor)
        collision = create_collision(customer_data, "REDACTED", trapdoor)
        end = time.perf_counter()
        cham_time = end - start

        # ----------------- Blockchain Update Timing ----------------- #
        start = time.perf_counter()
        tx = contract.functions.redactCustomer(customer_id).transact({"from": account.address})
        receipt = web3.eth.wait_for_transaction_receipt(tx)
        end = time.perf_counter()
        blockchain_time = end - start

        benchmark_results[customer_id] = {
            "ECC Time (s)": ecc_time,
            "Multiplicative Hash Time (s)": mult_hash_time,
            "ABE Time (s)": abe_time,
            "Chameleon Hash Time (s)": cham_time,
            "Blockchain Update Time (s)": blockchain_time
        }

    except ContractLogicError as e:
        print(f"Customer {customer_id} does not exist or is already redacted. Skipping... Error: {e}")
        continue

# ----------------- Display Results ----------------- #
df = pd.DataFrame.from_dict(benchmark_results, orient="index")
print(df)
