import string
import math
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def calculate_entropy(password, char_set_size):
    L = len(password)
    H = math.log2(char_set_size ** L)
    return H

def generate_quantum_password(length=12, use_digits=True, use_uppercase=True, use_special=True):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    special = string.punctuation

    char_set = lower
    if use_digits:
        char_set += digits
    if use_uppercase:
        char_set += upper
    if use_special:
        char_set += special

    charset_len = len(char_set)
    if charset_len == 0:
        raise ValueError("Character set cannot be empty.")

    n_bits = max(math.ceil(math.log2(charset_len)), 1)

    total_bits = length * n_bits
    qc = QuantumCircuit(total_bits, total_bits)
    qc.h(range(total_bits))  
    qc.measure_all()  

    simulator = AerSimulator()
    result = simulator.run(qc, shots=1).result()
    counts = result.get_counts(qc)

    if not counts:
        raise ValueError("Quantum circuit did not produce any measurement results.")

    bitstring = list(counts.keys())[0]
    bitstring = bitstring.replace(" ", "")

    password = []
    for i in range(length):
        start = i * n_bits
        end = start + n_bits
        segment = bitstring[start:end]

        rand_index = int(segment, 2)
        password.append(char_set[rand_index % charset_len])

    password_str = ''.join(password)
    entropy = calculate_entropy(password_str, charset_len)
    return password_str, entropy

def main():
    print("Welcome to the Quantum Password Generator!")
    
    while True:
        try:
            length = int(input("Enter the password length: "))
            if length <= 0:
                print("Password length must be a positive integer. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    use_digits = input("Include digits? (y/n): ").lower() == 'y'
    use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
    use_special = input("Include special characters? (y/n): ").lower() == 'y'

    try:
        print("\nGenerating your quantum password...")
        password, entropy = generate_quantum_password(
            length=length,
            use_digits=use_digits,
            use_uppercase=use_uppercase,
            use_special=use_special
        )
        print(f"\nGenerated Password: {password}")
        print(f"Entropy: {entropy:.2f} bits")
    except ValueError as e:
        print(f"Error: {e}")

if _name_ == "_main_":
    main()