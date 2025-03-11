import numpy as np

from qiskit import QuantumCircuit, transpile, assemble
from qiskit.visualization import circuit_drawer

from qiskit_aer import Aer

from qiskit.circuit.library import MCXGate



def create_maze_oracle(maze):
    """Creates a quantum oracle representing the maze."""
    rows, cols = maze.shape
    n_qubits = rows * cols
    qc = QuantumCircuit(n_qubits)

    wall_indices = [r * cols + c for r in range(rows) for c in range(cols) if maze[r, c] == 0]

    if not wall_indices:
        return qc.to_gate(label="MazeOracle")

    for idx in wall_indices:
        qc.x(idx)

    qc.h(wall_indices)
    if len(wall_indices) == 1:
        qc.z(wall_indices[0])
    else:
        controls = wall_indices[:-1]
        target = wall_indices[-1]
        qc.append(MCXGate(len(controls)), controls + [target])
        qc.z(target)
        qc.append(MCXGate(len(controls)), controls + [target])
    qc.h(wall_indices)

    for idx in wall_indices:
        qc.x(idx)

    return qc.to_gate(label="MazeOracle")



def create_diffusion_operator(num_qubits):
    """Creates the diffusion operator for Grover's algorithm."""
    qc = QuantumCircuit(num_qubits)
    qc.h(range(num_qubits))
    qc.x(range(num_qubits))
    qc.h(num_qubits - 1)
    if num_qubits == 1:
        qc.z(0)
    else:
        controls = list(range(num_qubits - 1))
        target = num_qubits - 1
        qc.append(MCXGate(len(controls)), controls + [target])
        qc.z(target)
        qc.append(MCXGate(len(controls)), controls + [target])
    qc.h(num_qubits - 1)
    qc.x(range(num_qubits))
    qc.h(range(num_qubits))
    return qc.to_gate(label="Diffusion")



def solve_maze_grover(maze, start, end):
    """Solves the maze using Grover's algorithm."""
    rows, cols = maze.shape
    num_qubits = rows * cols
    start_index = start[0] * cols + start[1]
    end_index = end[0] * cols + end[1]

    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits)) # Initial Hadamard gates

    maze_oracle = create_maze_oracle(maze)
    diffusion = create_diffusion_operator(num_qubits)

    num_iterations = int(np.sqrt(float(2**num_qubits)) * np.pi / 4)

    for _ in range(num_iterations):
        qc.append(maze_oracle, range(num_qubits))
        qc.append(diffusion, range(num_qubits))

    qc.measure(range(num_qubits), range(num_qubits))

    simulator = Aer.get_backend('qasm_simulator')
    transpiled_qc = transpile(qc, simulator)
    job = simulator.run(transpiled_qc, shots=1024)
    result = job.result()
    counts = result.get_counts()

    most_frequent_outcome = max(counts, key=counts.get)
    solution_path = [(int(i) // cols, int(i) % cols) for i, bit in enumerate(reversed(most_frequent_outcome)) if bit == '1']

    return most_frequent_outcome, counts, solution_path, qc  # Return the quantum circuit



# Example usage (using the new maze matrix)
matrix = [
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [0, 1, 1, 1],
    [1, 1, 0, 1]
]

maze = np.array(matrix)
start = (0, 0)
end = (3, 3)

outcome, counts, solution, qc = solve_maze_grover(maze, start, end) # added qc to returned variables

print("Maze data:\n", maze)
print("Start:", start, "End:", end)
print("Most frequent outcome (binary):", outcome)
print("Solution path (coordinates):", solution)

# Visualize the quantum circuit
print("\nQuantum Circuit:")
print(qc) # Print the circuit text
circuit_drawer(qc, output='text') # Draw the circuit in text format
# or
# circuit_drawer(qc, output='mpl', filename='maze_grover_circuit.png') #draw the circuit as an image (requires matplotlib)
