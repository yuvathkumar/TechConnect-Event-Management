import hashlib
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_mobile(mobile):
    return len(mobile) == 10 and mobile.isdigit()

def encrypt_data(data):
    return cipher.encrypt(data.encode())

def decrypt_data(encrypted_data):
    return cipher.decrypt(encrypted_data).decode()