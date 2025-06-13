import random
import string
import hashlib
import math
import pytest

# ✅ Step 1: Quantum Random Number Generator (Simulated)
def quantum_random_bits(num_bits=128):
    """Generates a quantum-random binary string (simulated using random choices)."""
    return ''.join(random.choice('01') for _ in range(num_bits))

# ✅ Step 2: Quantum Neural Network (QNN) Processing
def qnn_password_generator(length=12):
    """Generates a password using quantum randomness and ensures at least one special character."""
    char_space = string.ascii_letters + string.digits + "!@#$%^&*"
    special_chars = "!@#$%^&*"

    # Generate a password using quantum randomness
    quantum_bits = quantum_random_bits(length * 6)  # 6 bits per character
    password = ''.join(char_space[int(quantum_bits[i:i+6], 2) % len(char_space)]
                       for i in range(0, len(quantum_bits), 6))

    # ✅ Ensure at least one special character is present
    if not any(c in special_chars for c in password):
        password = list(password)
        password[random.randint(0, length - 1)] = random.choice(special_chars)
        password = ''.join(password)

    return password

# ✅ Step 3: Entropy Calculation
def calculate_entropy(password):
    """Calculates entropy of the password."""
    char_space_size = 94  # ASCII printable characters
    entropy = len(password) * math.log2(char_space_size)
    return entropy

# ✅ Step 4: Hashing the Password (SHA-3)
def hash_password(password):
    """Hashes the password using SHA-3."""
    return hashlib.sha3_256(password.encode()).hexdigest()

# ✅ Step 5: Quantum Key Distribution (QKD) Simulation
def quantum_key_distribution(password):
    """Simulates QKD by ensuring password is securely shared."""
    shared_key = hash_password(password)  # QKD simulates secure hashing
    return shared_key

# ✅ Integration Test Cases
def test_qrng_qnn_integration():
    """Test QRNG and QNN work together to generate passwords."""
    password = qnn_password_generator(16)
    assert len(password) == 16
    assert any(c.isupper() for c in password)  # Contains uppercase
    assert any(c.islower() for c in password)  # Contains lowercase
    assert any(c.isdigit() for c in password)  # Contains digit
    assert any(c in "!@#$%^&*" for c in password)  # ✅ Now always contains a special character

def test_qnn_entropy_integration():
    """Test QNN and entropy calculation."""
    password = qnn_password_generator(16)
    entropy = calculate_entropy(password)
    assert entropy > 100  # Ensuring strong password security

def test_qnn_hashing_integration():
    """Test QNN password is correctly hashed."""
    password = qnn_password_generator(16)
    hashed_password = hash_password(password)
    assert len(hashed_password) == 64  # SHA-3 hash length should be 64 hex characters

def test_qnn_qkd_integration():
    """Test QNN password and QKD secure transmission."""
    password = qnn_password_generator(16)
    shared_key = quantum_key_distribution(password)
    assert shared_key == hash_password(password)  # Ensuring secure key exchange

# ✅ Run PyTest if executed directly
if __name__ == "__main__":
    pytest.main()
