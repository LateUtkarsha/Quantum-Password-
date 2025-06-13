# password_generation.py
"""
Converts the measured qubits into a password, 
plus optional SHA-3 hashing for additional security.
"""

import hashlib


def bits_to_password(bitstring, length=12, symbols="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+"):
    """
    Convert a bitstring to a password of 'length' characters,
    using the given 'symbols' set. 
    Here we show a 7-bit approach as an example.
    """
    needed_bits = length * 7
    # If bitstring too short, repeat or pad
    if len(bitstring) < needed_bits:
        repeats = needed_bits // len(bitstring) + 1
        bitstring = bitstring * repeats

    bitstring = bitstring[:needed_bits]
    
    num_symbols = len(symbols)
    chars = []
    for i in range(length):
        chunk = bitstring[i*7:(i+1)*7]  # chunk of 7 bits
        val = int(chunk, 2)  # integer from 0..127
        val %= num_symbols   # map into symbols range
        chars.append(symbols[val])

    return "".join(chars)




def sha3_hash_password(password: str):
    """
    Applies SHA3-256 hashing to the password for post-processing.
    """
    hash_obj = hashlib.sha3_256(password.encode('utf-8'))
    return hash_obj.hexdigest()

