import numpy as np
import scipy.stats as stats

# ✅ Generate a quantum-random bitstream (Replace with actual QRNG output)
def generate_random_bits(num_bits=1000):
    return np.random.randint(0, 2, size=num_bits, dtype=np.uint8)


# ✅ (2) Chi-Square Test for Uniformity
def chi_square_uniform_test(bitstream):
    observed_counts = np.bincount(bitstream, minlength=2)
    expected_counts = [len(bitstream) / 2] * 2
    chi_stat, p_value = stats.chisquare(observed_counts, expected_counts)
    return p_value  # Should be > 0.01 for randomness

# ✅ (3) Monobit Frequency Test (Bit Balance Test)
def monobit_test(bitstream):
    ones = np.count_nonzero(bitstream)
    zeros = len(bitstream) - ones
    S = abs(ones - zeros) / np.sqrt(len(bitstream))
    p_value = stats.norm.sf(S) * 2  # Two-tailed test
    return p_value  # Should be > 0.01 for randomness

# ✅ Run the Tests
bitstream = generate_random_bits(1000)  # Generate a 1000-bit quantum random sequence


chi_square_p_value = chi_square_uniform_test(bitstream)
monobit_p_value = monobit_test(bitstream)

# ✅ Display Results
print("\n📌 **Randomness Test Results:**")
print(f"✅ Chi-Square Test P-value: {chi_square_p_value:.4f} {'✔ PASSED' if chi_square_p_value > 0.01 else '❌ FAILED'}")
print(f"✅ Monobit Frequency Test P-value: {monobit_p_value:.4f} {'✔ PASSED' if monobit_p_value > 0.01 else '❌ FAILED'}")
