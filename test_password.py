import pytest
import string
import random
import hashlib

# ✅ Fixed Password Generation Function
def generate_password(length=12):
    """Generates a password that always includes at least one uppercase, one lowercase, one digit, and one special character."""
    if length < 4:
        raise ValueError("Password length must be at least 4 to include all character types.")

    # Guarantee at least one character from each required category
    uppercase = random.choice(string.ascii_uppercase)
    lowercase = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special_char = random.choice("!@#$%^&*")

    # Fill the remaining length with random choices from all sets
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
    remaining_chars = [random.choice(all_chars) for _ in range(length - 4)]

    # Combine all characters and shuffle
    password_list = [uppercase, lowercase, digit, special_char] + remaining_chars
    random.shuffle(password_list)

    return ''.join(password_list)

# ✅ Hash Function
def hash_password(password):
    """Applies SHA-3 for hashing"""
    return hashlib.sha3_256(password.encode()).hexdigest()

# ✅ Test function names MUST start with "test_"
def test_password_length():
    """Check if password has correct length"""
    password = generate_password(16)
    assert len(password) == 16

def test_password_character_set():
    """Ensure password contains at least one uppercase, lowercase, number, and symbol"""
    password = generate_password()
    assert any(c.isupper() for c in password)  # Contains at least one uppercase
    assert any(c.islower() for c in password)  # Contains at least one lowercase
    assert any(c.isdigit() for c in password)  # Contains at least one digit
    assert any(c in "!@#$%^&*" for c in password)  # Contains at least one special character

def test_password_hash():
    """Ensure SHA-3 produces correct hash length (256 bits = 64 hex chars)"""
    password = generate_password()
    hashed_password = hash_password(password)
    assert len(hashed_password) == 64  # ✅ Fix: Removed extra period `.`

# ✅ Run PyTest if executed directly
if __name__ == "__main__":
    pytest.main()
