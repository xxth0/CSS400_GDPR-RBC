import time
import random
import sympy
import hashlib
import pandas as pd
from ecdsa import SigningKey, NIST256p
from auth_proof_gen import rsa_authentication, ecc_authentication, qkd_authentication
from chameleon_hash import ChameleonHash
from zk_rollup import ZKRollup

# Function to simulate RSA authentication cost (Work [2])
def rsa_authentication():
    start_time = time.time()
    p = sympy.randprime(2**511, 2**512)  # 1024-bit prime
    q = sympy.randprime(2**511, 2**512)  # 1024-bit prime
    n = p * q
    e = 65537
    phi = (p-1) * (q-1)
    d = pow(e, -1, phi)
    message = b"auth_request"
    hashed = int(hashlib.sha256(message).hexdigest(), 16)
    signature = pow(hashed, d, n)
    auth_time = time.time() - start_time
    return auth_time

# Function to simulate Quantum Key Distribution (QKD) authentication cost (Work [6])
def qkd_authentication():
    start_time = time.time()
    key_bits = [random.randint(0, 1) for _ in range(256)]
    basis = [random.choice(["+", "x"]) for _ in range(256)]
    auth_time = time.time() - start_time
    return auth_time

def qkd_authentication_realistic():
    start_time = time.time()
    
    # Simulating quantum photon transmission delay (Real-world: ~10 microseconds per photon)
    num_photons = 256  # 256-bit key transmission
    transmission_delay = num_photons * (10e-6)  # Delay in seconds

    # Simulating Quantum Error Correction (Real-world: adds processing overhead)
    error_correction_delay = 0.0005  # Assumed extra processing time for error correction

    # Simulating Quantum Key Agreement (QKA) processing delay (complex key processing)
    qka_processing_delay = 0.001  # Assumed key negotiation time

    # Simulating Quantum Measurement Overhead (converting quantum states to usable key bits)
    quantum_measurement_delay = 0.0002  # Assumed overhead for classical key extraction

    total_qkd_time = transmission_delay + error_correction_delay + qka_processing_delay + quantum_measurement_delay
    auth_time = time.time() - start_time + total_qkd_time

    return auth_time

# Function to simulate ECC-based authentication proof generation (Work [13])
def ecc_authentication():
ecc_times = [ecc_authentication() for _ in range(iterations)]


# Function to simulate Zero-Knowledge Proof (ZKP) with ECC (Our Work: Algorithm 4)
def zk_rollup_authentication():
    zk_rollup = ZKRollup(private_key=123456)
    start_time = time.time()
    batch_proof = zk_rollup.generate_proof(["auth_request"] * iterations)  # Only one proof per batch
    zk_rollup_time = time.time() - start_time  # Measure only batch time
    return zk_rollup_time


# Run simulations multiple times
iterations = 10000
rsa_times = [rsa_authentication() for _ in range(iterations)]
qkd_times = [qkd_authentication() for _ in range(iterations)]
qkd_times_realistic = [qkd_authentication_realistic() for _ in range(iterations)]
ecc_times = [ecc_authentication() for _ in range(iterations)]
zk_rollup_times = [zk_rollup_authentication() for _ in range(iterations)]

# Store results in a DataFrame with Work Numbers
df_results = pd.DataFrame({
    "Work No. + Method": [
        "[2] RSA (1024-bit)",
        "[6] Quantum Key Distribution (QKD)",
        "[6] Quantum Key Distribution (QKD) realistic",
        "[13] Elliptic Curve (ECC)",
        "[Our Work] ZK-Rollup + ECC (Algorithm 4)"
    ],
    "Avg Computation Time (s)": [
        sum(rsa_times) / iterations,
        sum(qkd_times) / iterations,
        sum(qkd_times_realistic) / iterations,
        sum(ecc_times) / iterations,
        sum(zk_rollup_times) / iterations
    ],
    "Total Computation Time (s)": [
        sum(rsa_times),
        sum(qkd_times),
        sum(qkd_times_realistic),
        sum(ecc_times),
        sum(zk_rollup_times)
    ]
})


# Display the results
print(df_results)
