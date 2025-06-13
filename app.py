# app.py
from flask import Flask, render_template, request
import os
import mysql.connector

# If you are using Qiskit
from qiskit_aer import AerSimulator

# ---- Import your local modules ----
# These filenames should match your actual files.
from quantum_random import quantum_random_bitstring
from qnn_model import build_qnn_circuit
from password_generation import bits_to_password, sha3_hash_password
from validation import validate_password_against_common_patterns
from qkd_simulation import simulate_qkd

# (NEW) Import simplified entropy functions
from entropy_utils import calculate_classical_entropy, calculate_quantum_entropy

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Add your MySQL password if set
    'database': 'quantum_passwords'
}

def insert_password(hashed_password):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO passwords2 (hashed_password) VALUES (%s)"
        cursor.execute(query, (hashed_password,))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

@app.route('/')
def index():
    """
    Renders the index page with the form for password generation inputs.
    """
    return render_template('index.html')  # This should match your 'templates/index.html'

@app.route('/generate_password', methods=['POST'])
def generate_password():
    """
    Handles form submissions from index.html.
    1) Gathers user inputs for QNN and password parameters.
    2) Builds the QNN circuit and measures it to get bits.
    3) Constructs a symbol set based on user choices (lowercase, uppercase, digits, symbols).
    4) Generates the final password from the bits.
    5) (Optional) Hashes with SHA-3, validates, simulates QKD, logs steps.
    6) (NEW) Computes classical & quantum entropy from simple_entropy.py.
    7) Renders result.html with all relevant info.
    """

    # -------------------------------
    # 1) Gather parameters from form
    # -------------------------------
    num_qubits = int(request.form.get('num_qubits', 8))
    shots = int(request.form.get('shots', 1))
    password_length = int(request.form.get('password_length', 12))

    # Checkboxes for character sets
    include_lowercase = (request.form.get('include_lowercase') == 'yes')
    include_uppercase = (request.form.get('include_uppercase') == 'yes')
    include_digits = (request.form.get('include_digits') == 'yes')
    include_symbols = (request.form.get('include_symbols') == 'yes')

    # Additional toggles
    apply_sha3 = (request.form.get('apply_sha3') == 'yes')
    validate_common = (request.form.get('validate_common') == 'yes')
    qkd_sim = (request.form.get('qkd_sim') == 'yes')

    # Prepare a log to describe steps
    process_log = "=== Quantum Password Generation ===\n\n"
    process_log += f"User Inputs:\n"
    process_log += f" - Qubits: {num_qubits}\n"
    process_log += f" - Shots: {shots}\n"
    process_log += f" - Password Length: {password_length}\n"
    process_log += f" - Include Lowercase: {include_lowercase}\n"
    process_log += f" - Include Uppercase: {include_uppercase}\n"
    process_log += f" - Include Digits: {include_digits}\n"
    process_log += f" - Include Symbols: {include_symbols}\n"
    process_log += f" - Apply SHA-3?: {apply_sha3}\n"
    process_log += f" - Validate Common Patterns?: {validate_common}\n"
    process_log += f" - QKD Simulation?: {qkd_sim}\n\n"

    # ------------------------------------------------
    # 2) Build QNN circuit & measure to get random bits
    # ------------------------------------------------
    process_log += "[Step] Generating quantum-random seed...\n"
    seed_bits = quantum_random_bitstring(num_bits=16)  # Or whatever size you want
    process_log += f"Quantum Random Seed (16 bits): {seed_bits}\n"

    # Build your QNN circuit
    process_log += "[Step] Building QNN circuit...\n"
    qnn_circuit = build_qnn_circuit(num_qubits=num_qubits, random_seed=seed_bits)

    # Add measurement to each qubit
    measure_circuit = qnn_circuit.copy()
    for i in range(num_qubits):
        measure_circuit.measure(i, i)

    # Run the circuit
    process_log += "[Step] Simulating circuit...\n"
    simulator = AerSimulator()
    job = simulator.run(measure_circuit, shots=shots)
    result = job.result()
    counts = result.get_counts(measure_circuit)

    # If multiple shots, pick the outcome with highest frequency
    best_outcome = max(counts, key=counts.get)
    process_log += f"Measured State with Highest Frequency: {best_outcome}\n\n"

    # -----------------------------------------------------
    # 3) Construct symbol set from user character choices
    # -----------------------------------------------------
    chosen_symbols = ""
    if include_lowercase:
        chosen_symbols += "abcdefghijklmnopqrstuvwxyz"
    if include_uppercase:
        chosen_symbols += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if include_digits:
        chosen_symbols += "0123456789"
    if include_symbols:
        chosen_symbols += "!@#$%^&*()-_=+"

    # Fallback if user unselected everything
    if not chosen_symbols:
        chosen_symbols = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        process_log += "[WARN] No character sets chosen! Fallback to alphanumeric.\n"

    # ----------------------------------------------------------------
    # 4) Convert bits -> password (7 bits per character recommended)
    # ----------------------------------------------------------------
    process_log += "[Step] Generating final password...\n"
    password = bits_to_password(best_outcome, password_length, chosen_symbols)
    process_log += f"Initial Password: {password}\n"

    # --------------------------------
    # 5) Optional: Apply SHA-3 hashing
    # --------------------------------
    hashed_password = None
    if apply_sha3:
        hashed_password = sha3_hash_password(password)
        process_log += f"SHA-3 Hashed Password: {hashed_password}\n"

    # Insert the password and hashed password into the database
    if  password:
        insert_password( hashed_password)

    # 6) Optional: Validate Commonness
    validation_message = ""
    if validate_common:
        is_common = validate_password_against_common_patterns(password)
        validation_message = (
            "WARNING: Password is in the known common patterns!"
            if is_common else
            "OK: Password is not found in common patterns."
        )
        process_log += f"Validation: {validation_message}\n"

    # 7) Optional: QKD Simulation
    qkd_info = None
    if qkd_sim:
        process_log += "[Step] Running QKD Simulation...\n"
        qkd_results = simulate_qkd(password, num_qubits=96)  # or your desired qubits for QKD
        qkd_info = (
            f"Password: {qkd_results['password']}\n"
            f"Sender Basis: {qkd_results['sender_basis']}\n"
            f"Receiver Basis: {qkd_results['receiver_basis']}\n"
            f"Shared Key: {qkd_results['shared_key']}\n"
            f"Valid Bits: {qkd_results['valid_bits_count']} / {qkd_results['total_qubits']}"
        )
        process_log += "QKD Simulation completed.\n"

    # (NEW) 8) Calculate simplified classical & quantum entropies
    char_space_size = len(chosen_symbols)
    classical_entropy = calculate_classical_entropy(password_length, char_space_size)
    quantum_entropy   = calculate_quantum_entropy(password_length, char_space_size)
    process_log += f"\n[Entropy] Classical: {classical_entropy:.2f} bits, Quantum: {quantum_entropy:.2f} bits\n"

    # Final log
    process_log += "\n[Done] Password generation steps complete."

    # --------------------------------------
    # Render result with all relevant fields
    # --------------------------------------
    return render_template(
        'result.html',
        password=password,
        hashed_password=hashed_password,
        validation_message=validation_message,
        qkd_info=qkd_info,
        process_log=process_log,
        # Pass entropies to the template
        classical_entropy=classical_entropy,
        quantum_entropy=quantum_entropy
    )

if __name__ == '__main__':
    # Run the Flask app in debug mode (or production if you prefer).
    app.run(debug=True)