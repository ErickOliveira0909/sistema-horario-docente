import hashlib

def generate_password_hash(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def check_password_hash(hashed_password, password):
    return hashed_password == generate_password_hash(password)