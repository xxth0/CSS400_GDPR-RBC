import hashlib
import random
import sympy

# Chameleon Hash Function
class ChameleonHash:
    def __init__(self, p=None, g=None):
        if not p:
            self.p = sympy.nextprime(2**256)
        else:
            self.p = p
        if not g:
            self.g = random.randint(2, self.p - 1)
        else:
            self.g = g
        self.trapdoor_key = random.randint(2, self.p - 1)
        self.public_key = pow(self.g, self.trapdoor_key, self.p)

    def hash(self, message, r):
        H = int(hashlib.sha256(message.encode()).hexdigest(), 16)
        return (r - (self.public_key * H + self.g) % self.p) % self.p

    def generate_collision(self, old_message, new_message, old_r):
        H_old = int(hashlib.sha256(old_message.encode()).hexdigest(), 16)
        H_new = int(hashlib.sha256(new_message.encode()).hexdigest(), 16)
        new_r = (old_r + self.g - self.public_key * (H_new - H_old)) % self.p
        return new_r
