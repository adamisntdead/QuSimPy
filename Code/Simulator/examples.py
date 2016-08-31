from QuSim import QuantumRegister

#############################################
#                 Introduction              #
#############################################
# Here Will Be A Few Example of Different   #
# Quantum States / Algorithms, So You Can   #
# Get A Feel For How The Module Works, and  #
# Some Algorithmic Ideas                    #
#############################################

#############################################
#                 Swap 2 Qubits             #
#############################################
# Here, We Will Apply a Pauli-X Gate / NOT Gate
# To the first qubit, and then after the algorithm,
# it will be swapped to the second qubit.

Swap = QuantumRegister(2) # New Quantum Register of 2 qubits
Swap.applyGate('X', 1) # Apply The NOT Gate. If Measured Now, it should be 10

# Start the swap algorithm
Swap.applyGate('CNOT', 1, 2)
Swap.applyGate('H', 1)
Swap.applyGate('H', 2)
Swap.applyGate('CNOT', 1, 2)
Swap.applyGate('H', 1)
Swap.applyGate('H', 2)
Swap.applyGate('CNOT', 1, 2)
# End the swap algorithm

print('SWAP: ' + Swap.measure()) # Measure the State, Should be 01
