# Quantum Steganography Playground

**Team Members: Aanya, Divya, Sunanditha**

Welcome to the **Quantum Steganography Playground**! This Python program simulates encoding and decoding a message using quantum computing principles. Your message will be encoded into quantum states, and then decoded with error correction, optional decoy qubits, and potential hacker simulations.

 Requirements

Before running this program, ensure you have the following Python libraries installed:

- `cirq`: A Python library for quantum computing.
- `tqdm`: A Python library for showing progress bars.
- `getpass`: For securely prompting the user for input (built-in with Python).

You can install the required libraries using pip:

```bash
pip install cirq tqdm
```

How to Use

1. **Message Input**: The program securely prompts you to enter the message you'd like to encode. The input will be hidden during entry for privacy.

2. **Encoding Method**: You can choose between two encoding methods:
   - **Classical Encoding (0 -> |0⟩, 1 -> |1⟩)**: This method maps each bit of the message to a quantum bit (qubit) in the computational basis.
   - **Superposition Encoding (0 -> |+⟩, 1 -> |–⟩)**: This method places each qubit into a superposition state.

3. **Error Correction**: You have the option to use error correction by repeating each bit three times (repetition coding). This ensures that the message can be corrected in case of noise.

4. **Decoy Qubits**: If you'd like to simulate eavesdropping detection, you can add decoy qubits. The decoy qubits are used to check for potential interception by unauthorized parties.

5. **Simulate Quantum Transmission**: Once the quantum states are prepared, the program simulates quantum transmission by running a quantum circuit on a simulator.

6. **Hacker Simulation**: Optionally, you can simulate a hacker attempting to intercept the transmission. This will randomly alter some bits of the measured quantum state to simulate a hacking attempt.

7. **Decoy Verification**: If decoy qubits were added, the program will compare the expected and measured decoy bits to detect any potential eavesdropping.

8. **Message Decoding**: After transmission, the program will decode the quantum message and display the original message. If error correction was enabled, it will also correct any errors caused by noise or hacking.

Features

- **Quantum Encoding**: Supports both classical and superposition encoding.
- **Error Correction**: Allows for error correction through repetition coding.
- **Eavesdropper Detection**: Optionally adds decoy qubits for eavesdropper detection.
- **Hacker Simulation**: Simulates a hacking attempt that could alter the quantum message.
- **Progress Bar**: Shows progress during message encoding and quantum transmission.
- **Message Security**: The program ensures the privacy and security of the message throughout the encoding, transmission, and decoding process.

## Code Walkthrough

key Functions:

- `print_progress(message, delay)`: Displays a progress bar while simulating the encoding or quantum transmission process.
- `apply_encoding(q, bit, method)`: Applies the encoding to a qubit based on the selected method (classical or superposition).
- `cirq.Circuit()`: Builds the quantum circuit for encoding the message.
- `cirq.Simulator()`: Simulates the quantum circuit to obtain the final state after transmission.
- `measure`: Measures the qubits after quantum transmission to retrieve the encoded message.

Error Correction:
If error correction is enabled, each bit of the message is repeated three times. The final decoded message is based on the majority rule for the repeated bits.

Decoy Qubits:
Decoy qubits are added as a security measure to detect eavesdropping. The program will verify if the measured decoy qubits match the expected values.

### Hacker Simulation:
The hacker simulation randomly flips some of the measured bits to simulate a hacking attempt. You can choose whether to simulate a hacker attack or not.

Example Usage

```
==============================================
  Welcome to the Quantum Steganography Playground!
  Your message will be encoded into quantum states and then decoded!
==============================================

Enter the message you'd like to encode (input hidden): [your message]
Choose encoding method:
  (1) Classical (0 -> |0⟩, 1 -> |1⟩)
  (2) Superposition (0 -> |+⟩, 1 -> |–⟩)
Enter 1 or 2: [1/2]
Use error correction (repeat each bit 3 times)? (yes/no): yes
Add decoy qubits for eavesdropper detection? (yes/no): yes
Simulate a hacker attempt? (yes/no): no

🔹 Step 1: Message converted to binary: 0100100001100101011011000110110001101111
🔹 Error Correction Enabled: Each bit is repeated 3 times.
[progress bar]
✅ Quantum Transmission Completed.
🔐 No hacking attempt. Message remains secure.
Decoy Qubits Verification:
Measured Decoy Binary: 010101
Expected Decoy Binary: 010101
✅ No eavesdropping detected!
✅ Decoded Message: Hello
🔹 Quantum Steganography Simulation Complete!
```

 Conclusion

This simulation is a playful and educational example of how quantum mechanics can be used for secure communication through quantum steganography. It combines concepts of quantum encoding, error correction, eavesdropper detection, and hacker simulations to demonstrate the potential of quantum security methods.