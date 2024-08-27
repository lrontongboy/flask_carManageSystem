from hashlib import sha256
import os
import hashlib

def encrypt_password(password):
    salt = os.urandom(16)
    hash_obj = hashlib.sha256(salt + password.encode()).hexdigest()
    return salt.hex() + hash_obj


def check_password_hash(stored_hash, password):
    salt = bytes.fromhex(stored_hash[:32])
    stored_hash_value = stored_hash[32:]
    hash_obj = hashlib.sha256(salt + password.encode()).hexdigest()
    return stored_hash_value == hash_obj