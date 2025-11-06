# security.py
from passlib.hash import pbkdf2_sha256

def hash_password(password: str) -> str:
    # PBKDF2-SHA256: robusto y sin límite de 72 bytes
    return pbkdf2_sha256.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pbkdf2_sha256.verify(plain, hashed)
