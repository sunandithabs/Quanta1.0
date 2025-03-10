TEAM NAME : QUANTASTIC 4-1

CONTRIBUTORS:
1>VIKAS J
2>KARTHIK SRINIVAS
3>JOE KONATH

CONTACT:
8310135392
jvikas1123@gmail.com


A Sudoku puzzle solver using quantum computing leverages quantum algorithms and quantum hardware to solve Sudoku puzzles more efficiently than classical methods in certain cases.

Problem Formulation
Sudoku is a constraint satisfaction problem (CSP) where:
-> Each row, column, and 3×3 sub grid must contain numbers 1–9 without repetition.
-> The goal is to fill the empty cells while satisfying these constraints

This code implements a Quantum Sudoku solver that combines traditional sudoku-solving techniques with quantum computing principles. Here's what it does:

The QuantumSudoku class creates and manages sudoku puzzles where empty cells are treated as being in quantum superposition of multiple possible values.
It uses Qiskit (a quantum computing framework) to create actual quantum circuits that represent the possible values for each cell.
The QuantumSudokuSolver class implements a hybrid approach to solving puzzles:

First applies basic sudoku strategies (naked singles, hidden singles)
Then uses quantum measurements for cells with few possibilities
Finally falls back to classical backtracking for remaining cells


The CustomQuantumSudoku class allows users to input their own sudoku puzzles.
The code includes interactive functions for inputting puzzles, visualizing the solution process, and measuring the time taken to solve.

The quantum approach is particularly interesting because it uses quantum superposition and measurement to explore possible values for cells, potentially offering a different way to solve sudoku compared to purely classical methods.