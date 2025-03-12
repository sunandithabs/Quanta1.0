import numpy as np
from qiskit import Aer, execute
from qiskit.optimization import QuadraticProgram
from qiskit.algorithms.optimizers import COBYLA
from qiskit.algorithms import QAOA
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.primitives import Sampler
from qiskit.algorithms.minimum_eigensolvers import QAOA
from qiskit.circuit.library import EfficientSU2
from qiskit_optimization.translators import from_docplex_mp
from docplex.mp.model import Model
import random

# Step 1: Generate a random distance matrix
def generate_distance_matrix(num_locations, max_distance=10):
    distance_matrix = np.random.randint(1, max_distance, size=(num_locations, num_locations))
    np.fill_diagonal(distance_matrix, 0)  # No self-travel cost
    return distance_matrix

# Step 2: Generate a QUBO problem for QAOA
def create_qubo_problem(distance_matrix):
    num_locations = len(distance_matrix)
    mdl = Model("Route Optimization")
    x = mdl.binary_var_list(num_locations, name="x")
    
    # Objective Function: Minimize total distance
    cost = sum(distance_matrix[i][j] * x[i] * x[j] for i in range(num_locations) for j in range(i + 1, num_locations))
    mdl.minimize(cost)
    
    return from_docplex_mp(mdl)

# Step 3: Solve using QAOA
def solve_qaoa(qubo_problem):
    sampler = Sampler()
    qaoa = QAOA(sampler=sampler, optimizer=COBYLA())
    qaoa_solver = MinimumEigenOptimizer(qaoa)
    result = qaoa_solver.solve(qubo_problem)
    return result

# Main Execution
num_locations = 5
distance_matrix = generate_distance_matrix(num_locations)
qubo_problem = create_qubo_problem(distance_matrix)
result = solve_qaoa(qubo_problem)

# Print Results
print("Distance Matrix:")
print(distance_matrix)
print("\nOptimal Route:", result)
