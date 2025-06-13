import numpy as np
import qiskit
from qiskit import QuantumCircuit, Aer, transpile, execute
from qiskit.circuit.library import EfficientSU2, RealAmplitudes
from qiskit_machine_learning.algorithms.classifiers import VQC
from qiskit_machine_learning.kernels import QuantumKernel
from qiskit.utils import algorithm_globals
from qiskit.algorithms.optimizers import COBYLA
import hashlib
import random
import pandas as pd
import re
from scipy.stats import entropy
from cryptography.hazmat.primitives import hashes

# -------------------------------
# 1. Load & Preprocess Password Data
# -------------------------------
def load_password_dataset(file_path):
    with open(file_path, encoding="latin-1") as f:
        passwords = f.readlines()
    return [p.strip() for p in passwords if len(p.strip()) == 12 and re.match(r"^[a-zA-Z0-9!@#$%^&*()]+$", p)]

# Example dataset (RockYou + Quantum Random)
rockyou_passwords = load_password_dataset("rockyou.txt")[:5000]
quantum_random_passwords = ["4sXz@9!B5k&", "Wq2*Lp9vX#1", "Zy7&dF#X8Qp", "Pm@L$9vT2Q7", "Xp5&Z@Y8q3L"]
final_passwords = rockyou_passwords + quantum_random_passwords

# -------------------------------
# 2. Quantum Encoding of Passwords
# -------------------------------
char_map = {char: format(idx, "06b") for idx, char in enumerate("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()")}

def password_to_qubits(password):
    return [int(bit) for char in password for bit in char_map[char]]

quantum_data = np.array([password_to_qubits(pwd) for pwd in final_passwords])

# -------------------------------
# 3. Define QNN Architecture
# -------------------------------
num_qubits = 16
qnn_circuit = EfficientSU2(num_qubits, entanglement="full", reps=3)

# Apply Hadamard Gates (Superposition)
for qubit in range(num_qubits):
    qnn_circuit.h(qubit)

# Apply Parameterized Rotations (Ry, Rz)
qnn_circuit.rx(np.pi / 4, range(num_qubits))
qnn_circuit.rz(np.pi / 4, range(num_qubits))

# Apply CNOT (Entanglement)
for i in range(num_qubits - 1):
    qnn_circuit.cx(i, i + 1)

# Measure Output
qnn_circuit.measure_all()

# -------------------------------
# 4. Train QNN with Variational Quantum Circuit (VQC)
# -------------------------------
quantum_kernel = QuantumKernel(feature_map=qnn_circuit, quantum_instance=Aer.get_backend("aer_simulator"))
qnn_model = VQC(
    feature_map=qnn_circuit,
    ansatz=qnn_circuit,
    optimizer=COBYLA(maxiter=100),
    quantum_instance=Aer.get_backend("aer_simulator"),
)

labels = np.array([1] * len(quantum_random_passwords) + [0] * len(rockyou_passwords))
qnn_model.fit(quantum_data, labels)

# -------------------------------
# 5. Parameter Shift Rule (Quantum Backpropagation)
# -------------------------------
def parameter_shift_grad(theta_value):
    backend = Aer.get_backend('aer_simulator')

    # Shifted circuits
    qc_plus = qnn_circuit.bind_parameters({theta_value: theta_value + np.pi/2})
    qc_minus = qnn_circuit.bind_parameters({theta_value: theta_value - np.pi/2})

    # Execute both circuits
    job_plus = execute(qc_plus, backend, shots=1024).result().get_counts()
    job_minus = execute(qc_minus, backend, shots=1024).result().get_counts()

    # Convert measurement outcomes to expectation values
    exp_plus = job_plus.get('1', 0) / 1024
    exp_minus = job_minus.get('1', 0) / 1024

    # Compute gradient
    grad = (exp_plus - exp_minus) / 2
    return grad

# -------------------------------
# 6. Generate Secure Password Using QNN
# -------------------------------
def generate_secure_password():
    simulator = Aer.get_backend("aer_simulator")
    result = execute(qnn_circuit, simulator, shots=1).result()
    measured_password = list(result.get_counts().keys())[0]

    # Convert back to characters
    password = "".join([list(char_map.keys())[int(measured_password[i : i + 6], 2)] for i in range(0, len(measured_password), 6)])
    return password

secure_password = generate_secure_password()
print("Generated Secure Password:", secure_password)

# -------------------------------
# 7. Entropy-Based Security Evaluation
# -------------------------------
def shannon_entropy(password):
    char_probs = [password.count(c) / len(password) for c in set(password)]
    return -sum(p * np.log2(p) for p in char_probs)

def von_neumann_entropy(q_state):
    return -np.trace(np.dot(q_state, np.log2(q_state)))

shannon_value = shannon_entropy(secure_password)
print("Shannon Entropy:", shannon_value)

sim_q_state = np.array([[0.5, 0.5], [0.5, 0.5]])  # Example quantum state
von_neumann_value = von_neumann_entropy(sim_q_state)
print("Von Neumann Entropy:", von_neumann_value)

# -------------------------------
# 8. Secure Password Storage Using SHA-3
# -------------------------------
def hash_password(password):
    digest = hashes.Hash(hashes.SHA3_256())
    digest.update(password.encode())
    return digest.finalize().hex()

hashed_password = hash_password(secure_password)
print("SHA-3 Hashed Password:", hashed_password)

# -------------------------------
# 9. QKD-Based Secure Password Transport
# -------------------------------
def qkd_encrypt_password(password, qkd_key):
    return "".join(chr(ord(c) ^ ord(k)) for c, k in zip(password, qkd_key))

def qkd_decrypt_password(cipher_text, qkd_key):
    return "".join(chr(ord(c) ^ ord(k)) for c, k in zip(cipher_text, qkd_key))

qkd_key = generate_secure_password()[:12]  # Generate a quantum-secure key
encrypted_password = qkd_encrypt_password(secure_password, qkd_key)
print("QKD Encrypted Password:", encrypted_password)

decrypted_password = qkd_decrypt_password(encrypted_password, qkd_key)
print("Decrypted Password:", decrypted_password)
