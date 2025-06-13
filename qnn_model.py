# qnn_model.py
"""
Defines a small 'Quantum Neural Network' style circuit
with entangling gates. We can optionally incorporate
random seeds from quantum_random.py.
"""

import numpy as np
from qiskit import QuantumCircuit

def build_qnn_circuit(num_qubits=8, random_seed=None):
    """
    Build a minimal 'Quantum Neural Network' circuit with
    quantum perceptron-like layers (Hadamard, CNOT, rotation gates).
    
    :param num_qubits: number of qubits in the circuit
    :param random_seed: an optional bitstring used as 'seed' for angles
    :return: an unmeasured QuantumCircuit
    """
    qc = QuantumCircuit(num_qubits, num_qubits)

    # Example: interpret bits of random_seed as angles
    if random_seed:
        chunk_size = 4  # e.g., 4 bits => value in [0..15]
        # We only parse enough chunks to match the qubits
        for i in range(num_qubits):
            start = i*chunk_size
            end = start + chunk_size
            if end <= len(random_seed):
                angle_bits = random_seed[start:end]
                angle_val = int(angle_bits, 2)
                angle = angle_val * (np.pi / 8.0)
                # RX rotation
                qc.rx(angle, i)

    # Layer 1: put qubits in superposition
    for i in range(num_qubits):
        qc.h(i)

    # Layer 2: entangle neighboring qubits
    for i in range(num_qubits - 1):
        qc.cx(i, i+1)

    # Layer 3: add some rotations as "activation"
    for i in range(num_qubits):
        qc.rz(np.pi/3, i)  # constant angle for demonstration

    # Another round of CNOT in reverse
    for i in range(num_qubits - 1):
        qc.cx(num_qubits-1-i, num_qubits-2-i)

    return qc

