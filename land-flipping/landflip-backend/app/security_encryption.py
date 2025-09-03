import base64
import os
from cryptography.fernet import Fernet, InvalidToken

KEY = os.getenv("ENCRYPTION_KEY", "").encode()

_cipher = Fernet(KEY) if KEY else None

PREFIX = "enc:"

def encrypt_value(value: str | None) -> str | None:
    if not value:
        return value
    if not _cipher:
        return value
    token = _cipher.encrypt(value.encode())
    return PREFIX + base64.urlsafe_b64encode(token).decode()


def decrypt_value(value: str | None) -> str | None:
    if not value:
        return value
    if not _cipher:
        return value
    if not value.startswith(PREFIX):
        return value
    b64 = value[len(PREFIX):]
    try:
        token = base64.urlsafe_b64decode(b64.encode())
        return _cipher.decrypt(token).decode()
    except (InvalidToken, Exception):
        return None
