import numpy as np
import matplotlib.pyplot as plt

# Function for Classical Entropy (Shannon entropy formula: H = log2(n))
def classical_entropy(n):
    return np.log2(n)  # Classical entropy follows logarithmic growth

# Function for Quantum Entropy (Approximately 2x Classical Entropy)
def quantum_entropy(n):
    return 2 * np.log2(n)  # Quantum entropy is approximately twice classical entropy

# Function to Plot the Graph
def plot_entropy_comparison():
    charspace = np.arange(2, 1000, 50)  # Password character space increasing

    c_entropy = classical_entropy(charspace)
    q_entropy = quantum_entropy(charspace)

    plt.figure(figsize=(6, 4))
    plt.plot(charspace, c_entropy, label="Classical Entropy", color="r", linestyle="dashed")
    plt.plot(charspace, q_entropy, label="Quantum Entropy (QRNG)", color="g")

    plt.title("Quantum vs Classical Entropy with Password Charspace Growth")
    plt.xlabel("Password Character Space (n)")
    plt.ylabel("Entropy (bits)")
    plt.legend()
    plt.grid()
    plt.show()

# Run the Plot
plot_entropy_comparison()
