# simple_entropy.py
import math

def calculate_classical_entropy(length, char_space):
    """
    Returns a simplistic 'classical entropy' measure:
      length * log2(char_space)
    Example: If password length = 12, 
             char_space = 62 (a-z, A-Z, 0-9),
             classical_entropy = 12 * log2(62).
    """
    return length * math.log2(char_space)

def calculate_quantum_entropy(length, char_space):
    """
    Returns a simplistic 'quantum entropy' measure 
    by doubling the classical entropy result.
    This is just a demonstration placeholder 
    (actual quantum entropy is more complex).
    """
    classical_entropy = calculate_classical_entropy(length, char_space)
    return classical_entropy * 2

