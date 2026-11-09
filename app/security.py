from pwdlib import PasswordHash


# Recommended settings (Argon2) chosen by the library
password_hasher = PasswordHash.recommended()


def hash_password(plain_password: str) -> str:
    """Turn a plain password into a secure hash (safe to store in the DB)."""
    return password_hasher.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if a plain password matches a stored hash"""
    return password_hasher.verify(plain_password, hashed_password)