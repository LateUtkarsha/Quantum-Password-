import hashlib
import random
import string

def generate_password(length=12):
    """Simulates a QNN-generated password"""
    char_set = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(char_set) for _ in range(length))

def hash_password(password):
    """Applies SHA-3 for hashing"""
    return hashlib.sha3_256(password.encode()).hexdigest()

def collision_test(num_passwords=500):
    password_set = set()
    collision_count = 0

    for _ in range(num_passwords):
        password = generate_password()
        password_hash = hash_password(password)

        if password_hash in password_set:
            collision_count += 1
        else:
            password_set.add(password_hash)

    collision_rate = (collision_count / num_passwords) * 100
    print(f"Total Passwords Tested: {num_passwords}")
    print(f"Collisions Found: {collision_count}")
    print(f"Collision Rate: {collision_rate:.6f}%")

collision_test()
