import random
from math import e, log, pi, sqrt

import numpy as np


class gates:
    # Store complex number i here for easy access
    i = np.complex(0, 1)

    ####################################################
    #                    Gates                         #
    ####################################################

    # Pauli-X / Not Gate
    X = np.matrix([
        [0, 1],
        [1, 0]
    ])
    # Pauli-Y Gate
    Y = np.matrix([
        [0, -i],
        [i, 0]
    ])
    # Pauli-Z Gate
    Z = np.matrix([
        [1, 0],
        [0, -1]
    ])
    # Hadamard Gate
    H = np.multiply(1. / sqrt(2), np.matrix([
        [1, 1],
        [1, -1]
    ]))
    # Identity Gate
    Id = np.eye(2)
    # S & S Dagger Gate
    S = np.matrix([
        [1, 0],
        [0, i]
    ])
    SDagger = S.conjugate().transpose()
    # T & T Dagger / Pi over 8 Gate
    T = np.matrix([
        [1, 0],
        [0, e**(i * pi / 4.)]
    ])
    TDagger = T.conjugate().transpose()

    # CNOT Gate, Control is 0, Target is 1
    CNOT = np.matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ])

    ####################################################
    #                Helper Functions                  #
    ####################################################

    @staticmethod
    def printmatrix(title):
        gateStr = 'gates.' + title
        print(eval(gateStr))

    @staticmethod
    def generateGate(gate, numQubits, targetQubit):
        # Put these here for handyness
        identity = gates.Id
        mainGate = eval('gates.' + gate)

        # Check if there is no modification needed
        if numQubits == 1:
            return mainGate

        newMatrix = np.matrix('0 0')
        firstGate = identity

        for num in range(1, numQubits + 1):
            if num == 1:
                # If its the first, then we cant do anything untill the
                # Next itteration, so store the value
                if targetQubit == 1:
                    firstGate = mainGate
                else:
                    firstGate = identity
            elif num == 2:
                # If its the second itteration
                if targetQubit == 2:
                    newMatrix = np.kron(firstGate, mainGate)
                else:
                    newMatrix = np.kron(firstGate, identity)
            else:
                if targetQubit == num:
                    newMatrix = np.kron(newMatrix, mainGate)
                else:
                    newMatrix = np.kron(newMatrix, identity)
        return newMatrix


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
        self.measured = False

    # Delete This, as amplitudes should not be accessable
    def amps(self):
        return self.amplitudes

    def applyGate(self, gate, target):
        gateMatrix = gates.generateGate(gate, self.numQubits, target)
        self.amplitudes = np.dot(self.amplitudes, gateMatrix)

    def measure(self):
        if self.measured:
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
            self.measured = True
            return self.value


qureg = QuantumRegister(5)
qureg.applyGate('X', 1)
qureg.applyGate('H', 3)
qureg.applyGate('TDagger', 3)
qureg.applyGate('X', 5)
print(qureg.measure())
