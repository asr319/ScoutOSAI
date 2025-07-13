from cryptography.fernet import Fernet
import os

_KEY_ENV = "APP_ENCRYPTION_KEY"


def _get_key() -> bytes:
    key = os.getenv(_KEY_ENV)
    if not key:
        raise RuntimeError(f"{_KEY_ENV} environment variable not set")
    return key.encode()


def generate_key() -> str:
    """Return a new key suitable for the APP_ENCRYPTION_KEY env variable."""
    return Fernet.generate_key().decode()


def encrypt_text(text: str) -> str:
    f = Fernet(_get_key())
    return f.encrypt(text.encode()).decode()


def decrypt_text(token: str) -> str:
    f = Fernet(_get_key())
    return f.decrypt(token.encode()).decode()
