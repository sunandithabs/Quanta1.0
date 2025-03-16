import cirq
import random
import time
import getpass
from tqdm import tqdm

def print_progress(message, delay=1.5):
    for _ in tqdm(range(100), desc=message, bar_format="{l_bar}{bar} [Elapsed: {elapsed}]"):
        time.sleep(delay / 100)

# =======================
# Welcome & User Interface
# =======================
print("==============================================")
print("  Welcome to the Quantum Steganography Playground!")
print("  Your message will be encoded into quantum states and then decoded!")
print("==============================================\n")
time.sleep(1)

# Securely prompt the user for a message
message = getpass.getpass("Enter the message you'd like to encode (input hidden): ")

# Ask the user to choose the encoding method
encoding_method = input("\nChoose encoding method:\n  (1) Classical (0 -> |0⟩, 1 -> |1⟩)\n  (2) Superposition (0 -> |+⟩, 1 -> |–⟩)\nEnter 1 or 2: ").strip()
while encoding_method not in ['1', '2']:
    encoding_method = input("Please enter 1 or 2: ").strip()

# Ask if the user wants error correction (repetition coding)
use_error_correction = input("\nUse error correction (repeat each bit 3 times)? (yes/no): ").strip().lower().startswith('y')

# Ask if the user wants to add decoy qubits for eavesdropper detection
use_decoys = input("\nAdd decoy qubits for eavesdropper detection? (yes/no): ").strip().lower().startswith('y')

# =======================
# Step 1: Convert Message to Binary
# =======================
binary_message = "".join(format(ord(char), '08b') for char in message)
print("\n🔹 Step 1: Message converted to binary:", binary_message)
print_progress("Converting message to quantum states")

# Apply error correction if enabled
if use_error_correction:
    binary_message = ''.join(bit * 3 for bit in binary_message)
    print("\n🔹 Error Correction Enabled: Each bit is repeated 3 times.")
    time.sleep(1)

# =======================
# Step 2: Build Quantum Circuit
# =======================
num_qubits = len(binary_message)
qubits = [cirq.LineQubit(i) for i in range(num_qubits)]
circuit = cirq.Circuit()

def apply_encoding(q, bit, method):
    if method == '1':  # Classical encoding
        if bit == '1':
            circuit.append(cirq.X(q))
    else:  # Superposition encoding
        circuit.append(cirq.H(q))
        if bit == '1':
            circuit.append(cirq.Z(q))

for i, bit in enumerate(binary_message):
    apply_encoding(qubits[i], bit, encoding_method)

if encoding_method == '2':  # Superposition requires final Hadamard
    circuit.append(cirq.H.on_each(*qubits))

# =======================
# Step 3: Add Decoy Qubits (Optional)
# =======================
if use_decoys:
    decoy_qubits = [cirq.LineQubit(num_qubits + i) for i in range(num_qubits)]
    decoy_data = [(random.choice(["computational", "hadamard"]), random.choice(['0', '1'])) for _ in decoy_qubits]
    for dq, (basis, bit) in zip(decoy_qubits, decoy_data):
        if basis == "computational" and bit == '1':
            circuit.append(cirq.X(dq))
        elif basis == "hadamard":
            circuit.append(cirq.H(dq))
            if bit == '1':
                circuit.append(cirq.Z(dq))
            circuit.append(cirq.H(dq))
    qubits.extend(decoy_qubits)

# Measure all qubits
circuit.append(cirq.measure(*qubits, key='result'))

# =======================
# Step 4: Simulate Quantum Transmission
# =======================
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=1)
measured_bits = ''.join(str(bit) for bit in result.measurements['result'][0])
print("\n✅ Quantum Transmission Completed.")

# =======================
# Step 5: Hacker Simulation (Quantum Attack)
# =======================
hack_choice = input("\nSimulate a hacker attempt? (yes/no): ").strip().lower()
if hack_choice.startswith('y'):
    print("\n🚨 Hacker Attempt Detected! 🚨")
    hacked_bits = ""
    for i in range(len(measured_bits)):
        if random.choice([True, False]):  # 50% chance hacker measures in wrong basis
            hacked_bits += str(random.choice(['0', '1']))  # Random collapse
        else:
            hacked_bits += measured_bits[i]  # Correct measurement
    measured_bits = hacked_bits
    print("❌ Hacked Binary:", measured_bits)
    time.sleep(1)
else:
    print("\n🔐 No hacking attempt. Message remains secure.")

# =======================
# Step 6: Decoy Verification (If Used)
# =======================
if use_decoys:
    measured_decoy_bits = measured_bits[num_qubits:]
    expected_decoy_bits = ''.join(bit for _, bit in decoy_data)
    print("\nDecoy Qubits Verification:")
    print("Measured Decoy Binary:", measured_decoy_bits)
    print("Expected Decoy Binary:", expected_decoy_bits)
    if measured_decoy_bits == expected_decoy_bits:
        print("✅ No eavesdropping detected!")
    else:
        print("❌ Possible eavesdropping detected!")
    measured_bits = measured_bits[:num_qubits]

# =======================
# Step 7: Decode the Message
# =======================
decoded_binary = ""
if use_error_correction:
    for i in range(0, len(measured_bits), 3):
        group = measured_bits[i:i+3]
        decoded_binary += '1' if group.count('1') >= 2 else '0'
else:
    decoded_binary = measured_bits

decoded_message = "".join(chr(int(decoded_binary[i:i+8], 2)) for i in range(0, len(decoded_binary), 8))
print("\n✅ Decoded Message:", decoded_message)

print("\n🔹 Quantum Steganography Simulation Complete!")