import time
import hashlib
import random
import sympy
from ecdsa import SigningKey, NIST256p
from collections import OrderedDict

# Simulated Hyperledger Fabric Blockchain
class MockHyperledger:
    def __init__(self):
        self.ledger = OrderedDict()
    
    def add_transaction(self, tx_id, data):
        self.ledger[tx_id] = data
    
    def get_transaction(self, tx_id):
        return self.ledger.get(tx_id, None)

# Initialize blockchain
blockchain = MockHyperledger()