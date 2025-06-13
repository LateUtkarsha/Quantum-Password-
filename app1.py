from flask import Flask, render_template, request, redirect, url_for, session
import os
import mysql.connector
from qiskit_aer import AerSimulator
from quantum_random import quantum_random_bitstring
from qnn_model import build_qnn_circuit
from password_generation import bits_to_password, sha3_hash_password
from validation import validate_password_against_common_patterns
from qkd_simulation import simulate_qkd
from entropy_utils import calculate_classical_entropy, calculate_quantum_entropy

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure session management

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Add your MySQL password if set
    'database': 'quantum_passwords'
}

# Helper function to insert passwords into the database
def insert_password(hashed_password, user_id, shared_key=None):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO passwords3 (user_id, hashed_password, shared_key) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, hashed_password, shared_key))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Helper function to check user role (admin/user)
def check_role():
    if 'user_id' in session:
        user_id = session['user_id']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
        role = cursor.fetchone()
        cursor.close()
        conn.close()
        return role[0] if role else 'user'
    return 'guest'

@app.route('/')
def index():
    """Renders the index page with the form for password generation inputs."""
    return render_template('index.html')

@app.route('/generate_password', methods=['POST'])
def generate_password():
    """Handles form submissions from index.html for password generation."""
    # Gather parameters from form
    qkd_results = None 
    num_qubits = int(request.form.get('num_qubits', 8))
    shots = int(request.form.get('shots', 1))
    password_length = int(request.form.get('password_length', 12))

    include_lowercase = (request.form.get('include_lowercase') == 'yes')
    include_uppercase = (request.form.get('include_uppercase') == 'yes')
    include_digits = (request.form.get('include_digits') == 'yes')
    include_symbols = (request.form.get('include_symbols') == 'yes')

    apply_sha3 = (request.form.get('apply_sha3') == 'yes')
    validate_common = (request.form.get('validate_common') == 'yes')
    qkd_sim = (request.form.get('qkd_sim') == 'yes')

    # Initialize process log
    process_log = "=== Quantum Password Generation ===\n\n"

    # Step 1: Gather user inputs for QNN and password parameters
    process_log += f"User Inputs: {num_qubits} qubits, {shots} shots, {password_length} password length\n"

    # Generate quantum-random seed
    process_log += "[Step] Generating quantum-random seed...\n"
    seed_bits = quantum_random_bitstring(num_bits=16)
    process_log += f"Quantum Random Seed (16 bits): {seed_bits}\n"

    # Build QNN circuit
    process_log += "[Step] Building QNN circuit...\n"
    qnn_circuit = build_qnn_circuit(num_qubits=num_qubits, random_seed=seed_bits)

    # Run the QNN circuit
    measure_circuit = qnn_circuit.copy()
    for i in range(num_qubits):
        measure_circuit.measure(i, i)

    # Simulate the circuit to generate random bits
    process_log += "[Step] Simulating circuit...\n"
    simulator = AerSimulator()
    job = simulator.run(measure_circuit, shots=shots)
    result = job.result()
    counts = result.get_counts(measure_circuit)

    best_outcome = max(counts, key=counts.get)
    process_log += f"Measured State: {best_outcome}\n\n"

    # Step 2: Create a symbol set based on user selections
    chosen_symbols = ""
    if include_lowercase:
        chosen_symbols += "abcdefghijklmnopqrstuvwxyz"
    if include_uppercase:
        chosen_symbols += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if include_digits:
        chosen_symbols += "0123456789"
    if include_symbols:
        chosen_symbols += "!@#$%^&*()-_=+"

    if not chosen_symbols:
        chosen_symbols = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        process_log += "[WARN] No character sets chosen! Defaulting to alphanumeric.\n"

    # Step 3: Generate final password from bits
    process_log += "[Step] Generating final password...\n"
    password = bits_to_password(best_outcome, password_length, chosen_symbols)
    process_log += f"Initial Password: {password}\n"

    # Step 4: Apply SHA-3 hashing if needed
    hashed_password = None
    if apply_sha3:
        hashed_password = sha3_hash_password(password)
        process_log += f"SHA-3 Hashed Password: {hashed_password}\n"

    # Step 5: Insert password into the database
    user_id = session.get('user_id', None)  # Get the logged-in user ID
    if hashed_password and user_id:  
        # QKD Simulation for Secure Transport
        shared_key = None
        if qkd_sim:
            process_log += "[Step] Running QKD Simulation...\n"
            qkd_results = simulate_qkd(password, num_qubits=96)  # 96 qubits for QKD simulation
            shared_key = qkd_results['shared_key']
            process_log += f"QKD Simulation completed. Shared Key: {shared_key}\n"

        # Insert into the database with optional QKD shared key
        insert_password(hashed_password, user_id, shared_key)

    # Step 6: Validate password against common patterns
    validation_message = ""
    if validate_common:
        is_common = validate_password_against_common_patterns(password)
        validation_message = "WARNING: Password is in common patterns!" if is_common else "OK: Password is unique."

    # Step 7: Calculate entropy values
    classical_entropy = calculate_classical_entropy(password_length, len(chosen_symbols))
    quantum_entropy = calculate_quantum_entropy(password_length, len(chosen_symbols))
    process_log += f"[Entropy] Classical: {classical_entropy:.2f} bits, Quantum: {quantum_entropy:.2f} bits\n"

    # Step 8: Render the result with the generated password, hash, QKD info, etc.
    return render_template(
        'result.html',
        password=password,
        hashed_password=hashed_password,
        validation_message=validation_message,
        qkd_info=qkd_results if qkd_sim else None,
        process_log=process_log,
        classical_entropy=classical_entropy,
        quantum_entropy=quantum_entropy
    )

# Admin route to view stored passwords (accessible only by admin)
@app.route('/admin')
def admin_dashboard():
    if check_role() != 'admin':
        return redirect(url_for('index'))  # Redirect to home if not admin

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passwords3")
    passwords = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('admin_dashboard.html', passwords=passwords)

if __name__ == '__main__':
    app.run(debug=True)
