# qkd_simulation.py
"""
A very simplified QKD-like simulation for demonstration.
Generates random bases, compares them to find a shared key.
"""

import random

def simulate_qkd(password, num_qubits=96):
    """
    Demonstration of a simplified QKD flow using password bits.
    :param password: password string
    :param num_qubits: how many bits to consider for QKD
    :return: dict with QKD results
    """
    # 1) Convert password into bits
    #    1 char => 8 bits, then truncate/pad to `num_qubits`
    pwd_bits = ''.join(format(ord(c), '08b') for c in password)
    if len(pwd_bits) < num_qubits:
        pwd_bits = pwd_bits.ljust(num_qubits, '0')
    else:
        pwd_bits = pwd_bits[:num_qubits]

    # 2) Generate random bases for sender & receiver
    bases_sender = ['X' if random.random() < 0.5 else '+' for _ in range(num_qubits)]
    bases_receiver = ['X' if random.random() < 0.5 else '+' for _ in range(num_qubits)]

    # 3) "Transmit" bits — in real QKD, we’d use qubit states
    #    For simplicity: we only keep bits where bases match
    valid_bits = []
    for i in range(num_qubits):
        if bases_sender[i] == bases_receiver[i]:
            valid_bits.append(pwd_bits[i])

    shared_key = "".join(valid_bits)

    results = {
        "password": password,
        "sender_basis": bases_sender,
        "receiver_basis": bases_receiver,
        "shared_key": shared_key,
        "valid_bits_count": len(valid_bits),
        "total_qubits": num_qubits
    }
    return results
