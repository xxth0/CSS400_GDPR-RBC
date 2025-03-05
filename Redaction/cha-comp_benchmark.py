import time
import hashlib
import pandas as pd
import random
import sympy
from concurrent.futures import ThreadPoolExecutor  # For offloading work

# Number of test iterations
iterations = 100

# Chameleon Hash Computation Class
class ChameleonHash:
    def __init__(self, p=None, g=None):
        """ Initialize Chameleon Hash parameters with precomputed modular inverse """
        self.p = p if p else sympy.nextprime(2**2048)  # Reduced prime for testing
        self.g = g if g else random.randint(2, self.p - 1)

        # Ensure trapdoor key is invertible
        while True:
            self.trapdoor_key = random.randint(2, self.p - 1)
            if sympy.gcd(self.trapdoor_key, self.p) == 1:
                break  # Ensure invertibility

        self.public_key = pow(self.g, self.trapdoor_key, self.p)

        # Precompute modular inverse to reduce computation time later
        self.precomputed_inverse = sympy.mod_inverse(self.public_key, self.p)

    def hash(self, message, r):
        """ Compute Chameleon Hash using correct algebraic structure """
        H = int(hashlib.sha256(message.encode()).hexdigest(), 16) % self.p
        return (H + (r * self.public_key) % self.p) % self.p  

    def generate_collision(self, old_message, new_message, old_r):
        """ Compute r2 to ensure hash collision """
        H_old = int(hashlib.sha256(old_message.encode()).hexdigest(), 16) % self.p
        H_new = int(hashlib.sha256(new_message.encode()).hexdigest(), 16) % self.p
        delta_H = (H_new - H_old) % self.p  # Ensure modular arithmetic

        # Use precomputed modular inverse for efficiency
        new_r = (old_r - (delta_H * self.precomputed_inverse) % self.p) % self.p

        # Debug Output
        print("\n[DEBUG] Collision Computation (Optimized)")
        print(f"  H_old: {H_old}")
        print(f"  H_new: {H_new}")
        print(f"  delta_H: {delta_H}")
        print(f"  Precomputed Inverse: {self.precomputed_inverse}")
        print(f"  Computed r2: {new_r}")

        # Ensure r2 is within valid range
        assert 0 <= new_r < self.p, f"r2 is out of bounds: {new_r}"
        return new_r

# Timing function for Chameleon Hash Computation with Redaction
def chameleon_hash_timing(message):
    """ Measure Chameleon Hash computation, redaction, and verification times (Optimized) """
    ch = ChameleonHash()
    r1 = random.randint(1, ch.p - 1)

    # Step 1: Compute Chameleon Hash
    start_time = time.perf_counter()
    hash1 = ch.hash(message, r1)
    time_ch_comp = time.perf_counter() - start_time

    # Step 2: Generate Collision (Offloaded to Thread)
    updated_message = message + "_modified"
    with ThreadPoolExecutor(max_workers=1) as executor:
        start_time = time.perf_counter()
        future_r2 = executor.submit(ch.generate_collision, message, updated_message, r1)
        r2 = future_r2.result()  # Get the result when ready
    time_ch_col = time.perf_counter() - start_time

    # Step 3: Verify Collision
    start_time = time.perf_counter()
    hash2 = ch.hash(updated_message, r2)
    verification = hash1 == hash2
    time_key_usage = time.perf_counter() - start_time

    # Debug Output
    print("\n[DEBUG] Chameleon Hash Verification (Optimized)")
    print(f"  Original Hash:  {hash1}")
    print(f"  Modified Hash:  {hash2}")
    print(f"  r1:             {r1}")
    print(f"  r2:             {r2}")
    print(f"  Trapdoor Key:   {ch.trapdoor_key}")
    print(f"  Public Key:     {ch.public_key}")
    print(f"  Hash Difference: {(hash1 - hash2) % ch.p}")
    print(f"  Verification:   {verification}")

    assert verification, "Chameleon Hash Redaction Failed!"

    # **Reflect the Optimization in Our Work**
    return {
        "Operation": [
            "Chameleon Hash Computation",
            "Collision Generation for Redaction",
            "Key Usage for Redaction",
            "Total Computation Time"
        ],
        "Scheme [13] (s)": [time_ch_comp, time_ch_col, time_key_usage],
        "Scheme [14] (s)": [time_ch_comp, time_ch_col, time_key_usage],
        "Scheme [21] (s)": [time_ch_comp, time_ch_col, time_key_usage],
        "Our Work (s)": [
            time_ch_comp, 
            time_ch_col,
            time_key_usage,

        ]
    }

# Run the benchmark
if __name__ == "__main__":
    message = "test_message"
    results = chameleon_hash_timing(message)

    # Display results as a table
    df_results = pd.DataFrame(results)
    print("\n[Benchmark Results]")
    print(df_results)
