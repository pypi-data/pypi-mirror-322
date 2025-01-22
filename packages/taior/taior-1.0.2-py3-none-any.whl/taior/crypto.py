from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

def generate_private_key():
    return x25519.X25519PrivateKey.generate()

def derive_shared_key(private_key, peer_public_key):
    return private_key.exchange(peer_public_key)

def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

def sign_data(private_key, data):
    return private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

def hash_data(data):
    return sha256(data.encode()).hexdigest()

def verify_data_integrity(original_data, received_hash):
    return hash_data(original_data) == received_hash

def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))  # Asegúrate de que data sea bytes
    return cipher.iv + ct_bytes   

def decrypt_data(encrypted_data, key):
    iv = encrypted_data[:AES.block_size] 
    ct = encrypted_data[AES.block_size:]   
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size)  # Asegúrate de que el resultado sea bytes