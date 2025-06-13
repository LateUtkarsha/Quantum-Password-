# main.py
"""
Demonstrates a Quantum Neural Network approach to password generation
using the modern Qiskit AerSimulator instead of the legacy 'execute' function.
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Local modules
from quantum_random import quantum_random_bitstring
from qnn_model import build_qnn_circuit
from password_generation import bits_to_password, sha3_hash_password
from qkd_simulation import simulate_qkd
from validation import validate_password_against_common_patterns


def main():
    # 1) Generate a quantum-random seed for the QNN
    seed_bits = quantum_random_bitstring(num_bits=16)
    print(f"[1] QRNG Seed bits: {seed_bits}")

    # 2) Build the QNN circuit with that seed (8 qubits for demonstration)
    qnn_circuit = build_qnn_circuit(num_qubits=8, random_seed=seed_bits)

    # 3) Copy the QNN circuit and add measurement to all qubits
    measure_circuit = qnn_circuit.copy()
    for i in range(8):
        measure_circuit.measure(i, i)

    # 4) Use the modern AerSimulator
    simulator = AerSimulator()
    job = simulator.run(measure_circuit, shots=1)
    result = job.result()

    # get_counts() expects the same circuit reference
    counts = result.get_counts(measure_circuit)
    measured_state = list(counts.keys())[0]  # e.g. "01010111"

    print(f"[2] Measured Qubit State: {measured_state}")

    # 5) Convert measured bits -> password (length 12 by default)
    password = bits_to_password(measured_state, password_length=12)
    print(f"[3] Raw QNN Password: {password}")

    # 6) Optional: apply SHA-3 hashing
    hashed_pass = sha3_hash_password(password)
    print(f"[4] SHA-3 Hashed Password: {hashed_pass}")

    # 7) QKD simulation using the generated password (96 bits for example)
    qkd_results = simulate_qkd(password, num_qubits=96)
    print("\n[5] QKD Simulation Results:")
    print(f"   Password: {qkd_results['password']}")
    print(f"   Sender Basis: {qkd_results['sender_basis']}")
    print(f"   Receiver Basis: {qkd_results['receiver_basis']}")
    print(f"   Shared Key: {qkd_results['shared_key']}")
    print(f"   Valid Bits: {qkd_results['valid_bits_count']} / {qkd_results['total_qubits']}")

    # Now validate against common patterns
    is_common = validate_password_against_common_patterns(password, "common_patterns.txt")
    if is_common:
        print("[WARNING] Generated password appears in common_patterns.txt!")
    else:
        print("[OK] Generated password does not match known common patterns.")


if __name__ == "__main__":
    main()
