# Re-import necessary libraries since execution state was reset
import numpy as np
import matplotlib.pyplot as plt

# Quantum vs Classical Entropy Calculation
qubits = np.arange(1, 11)  # Number of qubits
classical_entropy = np.log2(qubits)  # Classical entropy follows log2 scaling
quantum_entropy = qubits  # Quantum entropy scales linearly due to superposition

# Plot Quantum vs Classical Entropy
plt.figure(figsize=(8, 5))
plt.plot(qubits, classical_entropy, 'ro-', label="Classical Entropy (log2(N))")
plt.plot(qubits, quantum_entropy, 'bo-', label="Quantum Entropy (N)")
plt.xlabel("Number of Bits / Qubits")
plt.ylabel("Entropy (H)")
plt.title("Quantum vs Classical Entropy Growth")
plt.legend()
plt.grid(True)
plt.show()

# Performance Comparison of Quantum Algorithms
algorithms = ['Grover’s Algorithm', 'QKD', 'QRNG', 'QNN']
performance = [2, 10, 9, 12]  # Hypothetical performance measures

plt.figure(figsize=(8, 5))
plt.bar(algorithms, performance, color=['blue', 'green', 'red', 'purple'])
plt.xlabel("Quantum Algorithm")
plt.ylabel("Entropy Generation Capability")
plt.title("Comparison of QNN, QRNG, QKD, and Grover’s Algorithm")

for i, v in enumerate(performance):
    plt.text(i, v + 0.2, str(v), ha='center', color='black')

plt.grid(axis='y')
plt.show()
