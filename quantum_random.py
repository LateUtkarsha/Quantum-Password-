# quantum_random.py
"""
Generates a quantum-random bitstring using Qiskit's AerSimulator (modern approach).
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def quantum_random_bitstring(num_bits=64):
    """
    Generates a quantum random bitstring using Qiskit's AerSimulator.
    :param num_bits: number of qubits/bits to measure
    :return: a string of '0'/'1' of length `num_bits`
    """
    # 1) Create a quantum circuit with `num_bits` qubits + classical bits
    qc = QuantumCircuit(num_bits, num_bits)

    # 2) Apply Hadamard to each qubit
    for i in range(num_bits):
        qc.h(i)

    # 3) Measure each qubit into a classical register
    for i in range(num_bits):
        qc.measure(i, i)

    # 4) Use AerSimulator instead of old `execute`
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1)
    result = job.result()

    # 5) There will be exactly 1 measurement outcome since shots=1
    counts = result.get_counts(qc)
    measured_string = list(counts.keys())[0]  # e.g. "0101101101"
    return measured_string
