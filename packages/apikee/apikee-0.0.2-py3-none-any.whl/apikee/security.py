from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from os import urandom
from base64 import urlsafe_b64encode, urlsafe_b64decode
from .config import Config

IV_LENGTH = 12
SALT = b"secure_salt"


def derive_encryption_key() -> bytes:
    """Derive an encryption key from the master secret."""
    master_secret = Config.secret
    if not master_secret:
        raise ValueError("Master secret not configured. Set `APIKEE_SECRET` in the environment or configure it dynamically.")
    kdf = Scrypt(salt=SALT, length=32, n=2**14, r=8, p=1, backend=default_backend())
    return kdf.derive(master_secret.encode("utf-8"))


def generate_key(name: str) -> dict:
    """Generate an API key and a corresponding encrypted key ID."""
    random_string = urlsafe_b64encode(urandom(16)).decode("utf-8").rstrip("=")
    api_key = f"{name}_{random_string}"

    encryption_key = derive_encryption_key()
    iv = urandom(IV_LENGTH)

    cipher = Cipher(algorithms.AES(encryption_key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(api_key.encode()) + encryptor.finalize()

    return {
        "apiKey": api_key,
        "keyId": f"{urlsafe_b64encode(iv).decode()}:{urlsafe_b64encode(encrypted).decode()}:{urlsafe_b64encode(encryptor.tag).decode()}",
    }


def validate_key(api_key: str, key_id: str) -> bool:
    """Validate an API key against its key ID."""
    try:
        iv_b64, encrypted_b64, tag_b64 = key_id.split(":")
        iv = urlsafe_b64decode(iv_b64)
        encrypted = urlsafe_b64decode(encrypted_b64)
        tag = urlsafe_b64decode(tag_b64)

        encryption_key = derive_encryption_key()

        cipher = Cipher(algorithms.AES(encryption_key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(encrypted) + decryptor.finalize()

        return api_key == decrypted.decode("utf-8")
    except Exception as e:
        return False
