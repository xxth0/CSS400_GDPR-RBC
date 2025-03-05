import time
import hashlib
import pandas as pd
from ecdsa import SigningKey, NIST256p
from auth_proof_gen import ecc_authentication
from zk_rollup import ZKRollup

# Number of test iterations
iterations = 1

# Measure ECC authentication time
ecc_times = [ecc_authentication() for _ in range(iterations)]

# Measure ZK-Rollup batch proof generation time
zk_rollup = ZKRollup(private_key=123456)
start_time = time.time()
batch_proof = zk_rollup.generate_proof(["auth_request"] * iterations)  # Only one proof per batch
zk_rollup_time = time.time() - start_time  # Measure only batch time

# Store results in a DataFrame
df_results = pd.DataFrame({
    "Work No. + Method": [
        "[13] Elliptic Curve (ECC)",
        "[Our Work] ZK-Rollup + ECC (Algorithm 4)"
    ],
    "Avg Computation Time (s)": [
        sum(ecc_times) / iterations,
        zk_rollup_time / iterations
    ],
    "Total Computation Time (s)": [
        sum(ecc_times),
        zk_rollup_time
    ]
})

# Display results
print(df_results)
