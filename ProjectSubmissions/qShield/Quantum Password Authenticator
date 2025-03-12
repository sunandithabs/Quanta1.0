%matplotlib inline
import numpy as np
import random
import string
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

def generate_bb84_key_qiskit(num_bits=10):
    """
    Simulates the BB84 quantum key distribution using Qiskit.
    """
    # Alice generates random bits and bases
    alice_bits = np.random.randint(2, size=num_bits)
    alice_bases = np.random.randint(2, size=num_bits)
    
    # Quantum Circuit Simulation
    key = []
    backend = Aer.get_backend('aer_simulator')

    for i in range(num_bits):
        # Create a new quantum circuit for each bit
        qc = QuantumCircuit(1, 1)

        # If Alice's bit is 1, apply X gate to the qubit
        if alice_bits[i] == 1:
            qc.x(0)

        # If Alice's basis is 1, apply H gate to the qubit
        if alice_bases[i] == 1:
            qc.h(0)

        # Measure the qubit
        qc.measure(0, 0)

        # Display the quantum circuit
        print(f"Quantum Circuit for bit {i+1} (Alice bit: {alice_bits[i]}, Alice basis: {alice_bases[i]}):")
        fig = qc.draw('mpl')  # Create the circuit visualization
        plt.show()  # Show the figure
        
        # Transpile and run the circuit using the Aer simulator
        t_qc = transpile(qc, backend)
        result = backend.run(t_qc, shots=1).result()

        # Bob's measurement
        bob_measurement = int(list(result.get_counts().keys())[0])

        # Bob randomly chooses a basis for measurement
        bob_basis = np.random.randint(2)

        # If Bob's basis matches Alice's, they keep the bit
        if bob_basis == alice_bases[i]:
            key.append(str(bob_measurement))

    return "".join(key)

def xor_encrypt_decrypt(data, key):
    """
    Encrypts or decrypts the given data using XOR with the provided key.
    """
    key_length = len(key)
    return ''.join(chr(ord(data[i]) ^ ord(key[i % key_length])) for i in range(len(data)))

def generate_random_password(length=12):
    """
    Generate a random secure password with uppercase, lowercase, digits, and symbols.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def simulate_qkd_authentication(password):
    try:
        qkd_key = generate_bb84_key_qiskit(16)  # Generate a quantum key
        print(f"Generated BB84 Key: {qkd_key}")

        encrypted_password = xor_encrypt_decrypt(password, qkd_key)
        print(f"Encrypted Password (XOR): {encrypted_password}")

        decrypted_password = xor_encrypt_decrypt(encrypted_password, qkd_key)
        print(f"Decrypted Password: {decrypted_password}")

        if decrypted_password == password:
            print("Authentication Successful! ✅")
        else:
            print("Authentication Failed! ❌")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    choice = input("Do you want to (1) Enter a password or (2) Generate a random password? ")
    if choice == "2":
        password = generate_random_password()
        print(f"Generated Password: {password}")
    else:
        password = input("Enter a password to authenticate: ")
    simulate_qkd_authentication(password)

if __name__ == "__main__":
    main()
