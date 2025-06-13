import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Grover's algorithm amplitude amplification function
def grover_amplitude_amplification(iterations, N):
    amplitudes = np.zeros(iterations)
    initial_amplitude = 1 / np.sqrt(N)
    amplitude = initial_amplitude
    
    for i in range(iterations):
        amplitude = np.sqrt(2) * amplitude * (1 - 1/N)  # Amplification formula
        amplitudes[i] = amplitude
        
    return amplitudes

# Function to visualize Grover's algorithm
def plot_grover_iterations():
    N = 16  # size of the database
    iterations = 10  # number of iterations
    amplitudes = grover_amplitude_amplification(iterations, N)
    
    fig, ax = plt.subplots()
    ax.set_title("Amplitude Amplification in Grover's Algorithm")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Amplitude")
    
    ax.plot(np.arange(iterations), amplitudes, label="Amplitude", color="b")
    ax.legend()
    
    plt.show()


# Animation of Grover's algorithm search process
def animate_grover():
    N = 16  # size of the database
    iterations = 10  # number of iterations
    amplitudes = grover_amplitude_amplification(iterations, N)
    
    fig, ax = plt.subplots()
    ax.set_xlim(0, iterations)
    ax.set_ylim(0, 1)
    ax.set_title("Grover's Algorithm: Amplitude Amplification Over Iterations")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Amplitude")
    
    line, = ax.plot([], [], lw=2, label="Amplitude", color="b")
    ax.legend()
    
    def init():
        line.set_data([], [])
        return line,
    
    def update(i):
        line.set_data(np.arange(i+1), amplitudes[:i+1])
        return line,
    
    ani = animation.FuncAnimation(fig, update, frames=iterations, init_func=init, blit=True)
    plt.show()

# Call the functions
plot_grover_iterations()  # Plotting Grover's algorithm
animate_grover()          # Animated visualization of Grover's algorithm
