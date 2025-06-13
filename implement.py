import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Grover's algorithm amplitude amplification function
def grover_amplitude_amplification(iterations, N):
    amplitudes = np.zeros(iterations)
    initial_amplitude = 1 / np.sqrt(N)
    amplitude = initial_amplitude
    
    for i in range(iterations):
        amplitude = np.sqrt(2) * amplitude * (1 - 1/N)  # Simplified amplification formula
        amplitudes[i] = amplitude
        
    return amplitudes

# 1. Grover's Algorithm: Amplitude Amplification Visualization
def plot_grover_iterations():
    N = 16  # Database size
    iterations = 10  # Number of iterations
    amplitudes = grover_amplitude_amplification(iterations, N)
    
    plt.figure(figsize=(6, 4))
    plt.plot(np.arange(iterations), amplitudes, label="Amplitude", color="b")
    plt.title("Grover's Algorithm: Amplitude Amplification")
    plt.xlabel("Iteration")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid()
    plt.show()

# 2. Security Comparison: QKD vs Grover's Search
def plot_security_comparison():
    iterations = np.arange(1, 11)
    grover_security = np.exp(-iterations / 3)  # Grover weakens against quantum encryption
    qkd_security = np.ones_like(iterations)  # QKD maintains strong security

    plt.figure(figsize=(6, 4))
    plt.plot(iterations, grover_security, label="Grover's Algorithm Security", color="r", linestyle="dashed")
    plt.plot(iterations, qkd_security, label="QKD Security", color="g")
    
    plt.title("Security: QKD vs Grover's Algorithm")
    plt.xlabel("Iteration")
    plt.ylabel("Security Strength")
    plt.legend()
    plt.grid()
    plt.show()

# 3. Randomness Quality: QRNG vs Classical RNG vs Grover Predictability
def plot_randomness_distribution():
    classical_rng = np.random.randint(0, 100, 1000)  # Classical RNG
    qrng = np.random.uniform(0, 100, 1000)  # Quantum RNG (More uniform)
    grover_prediction = np.random.choice([20, 40, 60, 80], 1000)  # Grover only searches specific elements

    plt.figure(figsize=(6, 4))
    plt.hist(classical_rng, bins=20, alpha=0.6, label="Classical RNG", color="blue")
    plt.hist(qrng, bins=20, alpha=0.6, label="QRNG (Quantum RNG)", color="green")
    plt.hist(grover_prediction, bins=20, alpha=0.6, label="Grover Predictable", color="red")
    
    plt.title("Randomness Quality: QRNG vs Classical RNG vs Grover")
    plt.xlabel("Generated Numbers")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid()
    plt.show()

# 4. Computational Efficiency: QNN vs Grover
def plot_computation_efficiency():
    methods = ['Grover’s Algorithm', 'QKD', 'QRNG', 'QNN']
    efficiency = [2, 9, 9, 12]  # Hypothetical performance scores

    plt.figure(figsize=(6, 4))
    plt.bar(methods, efficiency, color=['blue', 'green', 'red', 'purple'])
    
    plt.title("Computation & Security: QNN, QKD, QRNG vs Grover")
    plt.ylabel("Efficiency / Security Score")
    
    for i, v in enumerate(efficiency):
        plt.text(i, v + 0.2, str(v), ha='center', color='black')

    plt.grid()
    plt.show()

# Calling all graphs
plot_grover_iterations()      # Grover's Algorithm Amplitude
plot_security_comparison()    # Security Strength Comparison (Grover vs QKD)
plot_randomness_distribution() # Randomness Comparison (QRNG vs Classical vs Grover)
plot_computation_efficiency()  # Computation Efficiency (Grover vs QNN, QKD, QRNG)
