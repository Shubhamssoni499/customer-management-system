import re


# -----------------------------------------
# Email Validation
# -----------------------------------------
def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))


# -----------------------------------------
# Phone Validation (Simple Indian 10-digit)
# -----------------------------------------
def is_valid_phone(phone: str) -> bool:
    return phone.isdigit() and len(phone) == 10


# -----------------------------------------
# Name Validation (Allow only alphabets)
# -----------------------------------------
def is_valid_name(name: str) -> bool:
    return bool(re.match(r"^[A-Za-z\s]+$", name))


# -----------------------------------------
# Check Empty Value
# -----------------------------------------
def is_not_empty(value: str) -> bool:
    return value.strip() != ""


# -----------------------------------------
# Validate multiple required fields
# -----------------------------------------
def validate_required(data: dict, required_fields: list):
    """
    Checks if required fields are empty or missing.
    """
    for field in required_fields:
        if field not in data or not is_not_empty(data[field]):
            return False, f"{field} is required."
    return True, "OK"