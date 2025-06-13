import time
import random
import string

# Define the password generation function
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Measure execution time using time.perf_counter()
start_time = time.perf_counter()
for _ in range(500):  # Generate 500 passwords
    generate_password()
end_time = time.perf_counter()

avg_time = (end_time - start_time) / 500
print(f"Average Password Generation Time: {avg_time:.10f} seconds")
