import hashlib
import os

class ZKRollup:
    def __init__(self, private_key):
        self.private_key = private_key
        self.public_key = hashlib.blake2s(str(private_key).encode()).digest()  # Faster hashing
        self.precomputed_randoms = [int.from_bytes(os.urandom(32), "big") for _ in range(10000)]
        self.random_index = 0

    def generate_proof(self, messages):
        message_hashes = [hashlib.blake2s(m.encode()).digest() for m in messages]

        while len(message_hashes) > 1:
            message_hashes = [
                hashlib.blake2s(message_hashes[i] + message_hashes[i + 1]).digest()
                for i in range(0, len(message_hashes) - 1, 2)
            ]

        merkle_root = message_hashes[0]
        return merkle_root.hex()
