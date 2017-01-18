import random
import string
from math import e, log, pi, sqrt
from functools import reduce

import numpy as np


class gates:
    # Store complex number i here for easy access
    i = np.complex(0, 1)

    ####################################################
    #                    Gates                         #
    ####################################################
    singleQubitGates = {
        # Pauli-X / Not Gate
        'X': np.matrix([
            [0, 1],
            [1, 0]
        ]),
        # Pauli-Y Gate
        'Y': np.matrix([
            [0, -i],
            [i, 0]
        ]),
        # Pauli-Z Gate
        'Z': np.matrix([
            [1, 0],
            [0, -1]
        ]),
        # Hadamard Gate
        'H': np.multiply(1. / sqrt(2), np.matrix([
            [1, 1],
            [1, -1]
        ])),
        # Identity Gate
        'Id': np.eye(2),
        # S & S Dagger Gate
        'S': np.matrix([
            [1, 0],
            [0, i]
        ]),
        'SDagger': np.matrix([
            [1, 0],
            [0, i]
        ]).conjugate().transpose(),
        # T & T Dagger / Pi over 8 Gate
        'T': np.matrix([
            [1, 0],
            [0, e**(i * pi / 4.)]
        ]),
        'TDagger': np.matrix([
            [1, 0],
            [0, e**(i * pi / 4.)]
        ]).conjugate().transpose()
    }

    ####################################################
    #                Helper Functions                  #
    ####################################################

    @staticmethod
    def generateGate(gate, numQubits, qubit1, qubit2=1):
        if (gate == 'CNOT'):
            control = qubit1
            target = qubit2

            identity = np.eye(2)
            X = gates.singleQubitGates['X']
            # NaN is our 'C' from the multi qubit gate generation formula
            C = np.mat([
                [float('nan'), 0],
                [0, 1]
            ])

            # Set the gate order
            gateOrder = []
            for i in range(1, numQubits + 1):
                if (i == control):
                    gateOrder.append(C)
                elif (i == target):
                    gateOrder.append(X)
                else:
                    gateOrder.append(identity)

            # Generate the gate and then replace the NaNs to Id gates
            newGate = reduce(np.kron, gateOrder)

            n = newGate.shape[0]
            return np.mat([[newGate[i, j] if not np.isnan(newGate[i, j]) else 1 if i == j else 0 for j in range(n)] for i in range(n)])

        else:
            # Put these here for handyness
            identity = gates.singleQubitGates['Id']
            mainGate = gates.singleQubitGates[gate]

            gateOrder = []

            for i in range(1, numQubits + 1):
                if (i == qubit1):
                    gateOrder.append(mainGate)
                else:
                    gateOrder.append(identity)

            return reduce(np.kron, gateOrder)


class QuantumRegister:

    def __init__(self, numQubits):
        self.numQubits = numQubits
        # The number of amplitudes needed is 2^n,
        # Where N is the number of qubits. The np.zeros function
        # Creates a matrix of 0s, ie.
        # np.zeros(5) = [0, 0, 0, 0, 0]
        self.amplitudes = np.zeros(2**numQubits)
        # Set the chance of getting all Zeros to 1
        self.amplitudes[0] = 1
        # Set the fact it has not been measured
        self.value = False

    def applyGate(self, gate, qubit1, qubit2=-1):
        if self.measured:
            raise ValueError(
                'Cannot Apply Gate to a Measured Quantum Register')
        else:
            gateMatrix = gates.generateGate(
                gate, self.numQubits, qubit1, qubit2)
            self.amplitudes = np.dot(self.amplitudes, gateMatrix)

    def measure(self):
        if self.value:
            return self.value
        else:
            # Get this list of probabilities, by squaring the absolute
            # Value of the amplitudes
            self.probabilities = []
            for amp in np.nditer(self.amplitudes):
                probability = np.absolute(amp)**2
                self.probabilities.append(probability)
            # Now that we have the probabilities, we can use them to choose a list index,
            # Which actually we can convert to the states, as the list counts up in a binary pattern.
            # ie, if the list index was 3, well it would actually be 3 in binary, and then we can just append
            # The zeros to the state. To Choose a state, we need a list, so we
            # will make a new list:
            results = []
            for prob in self.probabilities:
                results.append(len(results))
            # Now we can choose and set the value, so when called again we get
            # the same result.
            self.value = np.binary_repr(
                np.random.choice(results, 1, p=self.probabilities),
                self.numQubits
            )
            return self.value
