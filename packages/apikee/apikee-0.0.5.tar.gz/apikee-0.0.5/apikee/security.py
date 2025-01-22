from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64, os
from config import config

def derive_encryption_key():
    """Derives a 256-bit encryption key from the master secret."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'secure_salt',
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(config['secret'].encode())

def generate_key(name: str):
    """Generates a secure API key and its corresponding keyId."""
    if not name:
        raise ValueError("Missing API key name.")

    random_string = base64.urlsafe_b64encode(os.urandom(24)).decode('utf-8').rstrip("=")  # Base64url for compactness
    api_key = f"{name}_{random_string}"

    encryption_key = derive_encryption_key()
    iv = os.urandom(12)  # Generate a random IV
    cipher = Cipher(algorithms.AES(encryption_key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    encrypted = encryptor.update(api_key.encode()) + encryptor.finalize()
    auth_tag = encryptor.tag

    # Generate the keyId in a compact format
    key_id = f"{base64.urlsafe_b64encode(iv).decode('utf-8').rstrip('=')}.{base64.urlsafe_b64encode(auth_tag).decode('utf-8').rstrip('=')}.{base64.urlsafe_b64encode(encrypted).decode('utf-8').rstrip('=')}"

    return {'apiKey': api_key, 'keyId': key_id}

def validate_key(api_key: str, key_id: str) -> bool:
    """Validates the API key against its keyId."""
    try:
        iv_base64, auth_tag_base64, encrypted_base64 = key_id.split('.')
        iv = base64.urlsafe_b64decode(iv_base64 + '==')
        auth_tag = base64.urlsafe_b64decode(auth_tag_base64 + '==')
        encrypted = base64.urlsafe_b64decode(encrypted_base64 + '==')

        encryption_key = derive_encryption_key()
        cipher = Cipher(algorithms.AES(encryption_key), modes.GCM(iv, auth_tag), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted = decryptor.update(encrypted) + decryptor.finalize()

        return api_key == decrypted.decode('utf-8')
    except Exception:
        return False  # Return False if decryption or validation fails
