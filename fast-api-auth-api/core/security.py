from passlib.context import CryptContext


# Helper class to handle password hashing and verification
ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return ctx.verify(plain_password, hashed_password)


def generate_hash_password(password: str) -> str:
    return ctx.hash(password)