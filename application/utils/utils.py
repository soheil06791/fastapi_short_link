from bcrypt import checkpw, hashpw, gensalt
from cryptography.fernet import Fernet
from base64 import urlsafe_b64decode, urlsafe_b64encode


def hash_password(password: str):
    hashed_password = hashpw(password.encode('utf-8'), gensalt())
    saved_password = urlsafe_b64encode(hashed_password).decode()
    return saved_password


def verify_password(password: str, saved_password: str):
    try:
        hashed_password = urlsafe_b64decode(saved_password.encode())
        if checkpw(password.encode('utf-8'), hashed_password):
            return True
    except:
        return False


def encode_crypto(user_id: int, key: str):
    primary_key = Fernet(key.encode('utf-8'))
    return primary_key.encrypt(str(user_id).encode('utf-8')).decode('utf-8')


def decode_crypto(uid_encode: str, key: str):
    primary_key = Fernet(key.encode('utf-8'))
    try:
        user_id = primary_key.decrypt(uid_encode.encode('utf-8')).decode('utf-8')
        return user_id
    except:
        return False


def read_and_encode_file(file_path):
    with open(file_path) as f:
        return f.read()
