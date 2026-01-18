import hashlib
import uuid
from datetime import datetime


# -----------------------------------------
# 1. Password Hashing (Simple + Secure)
# -----------------------------------------
def hash_password(password: str) -> str:
    """
    Converts plain text password to a hashed value (SHA256).
    Easy to explain: password hashing = security.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if entered password matches stored hashed password.
    """
    return hash_password(plain_password) == hashed_password


# -----------------------------------------
# 2. Unique ID Generator
# -----------------------------------------
def generate_id(prefix: str = "ID") -> str:
    """
    Generate simple unique IDs like: CUST-82BD290A
    """
    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"


# -----------------------------------------
# 3. Date & Time helper
# -----------------------------------------
def get_timestamp() -> str:
    """
    Returns current time in clean format for database.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# -----------------------------------------
# 4. Small helper for success/error message
# -----------------------------------------
def make_response(status: str, message: str, data=None):
    """
    Common format for returning results.
    """
    return {
        "status": status,
        "message": message,
        "data": data
    }