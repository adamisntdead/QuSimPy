import random
import string
from math import e, log, pi, sqrt

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
    def generateGate(gate, numQubits, qubit1, qubit2=-1):
        if (gate == 'CNOT' and qubit2 != -1):
            control = qubit1
            target = qubit2

            # Generates List of Combinations of each qubit. there is 2n of them.
            # Returns List in string form, in the variable opts
            opts = []
            for i in range(0, (2**numQubits)):
                opts.append(np.binary_repr(i, width=numQubits))

            # Goes through the list of possible binary strings, makes a new list of
            # What index maps to what
            mapList = []
            for index, option in enumerate(opts):
                nums = list(option)
                if nums[control - 1] == '1':
                    mapList.append([index, -1])
                else:
                    mapList.append([index, index])

            for j, index in enumerate(mapList):
                if index[1] == -1:
                    # Takes the option and splits to each charachter
                    firstList = list(opts[index[0]])

                    # Figure out if looking for 0 or 1
                    toFlip = '0'
                    if firstList[target - 1] == '0':
                        toFlip = '1'
                    elif firstList[target - 1] == '1':
                        toFlip = '0'

                    targetPattern = firstList
                    targetPattern[target - 1] = toFlip
                    # The String Searching For
                    targetPattern = ''.join(targetPattern)
                    # The Index of the new strng
                    mapList[j][1] = opts.index(targetPattern)

            # Generate Empty Matrix To Use To Create New One
            newMatrix = np.zeros((2**numQubits, 2**numQubits))

            # Go through the map of 1's and put them in
            for item in mapList:
                newMatrix.itemset((item[0], item[1]), 1)

            return np.asmatrix(newMatrix)
        else:
            # Put these here for handyness
            identity = gates.singleQubitGates['Id']
            mainGate = gates.singleQubitGates[gate]

            # Check if there is no modification needed
            if numQubits == 1:
                return mainGate

            newMatrix = np.matrix('0 0')
            firstGate = identity

            for num in range(1, numQubits + 1):
                if num == 1:
                    # If its the first, then we cant do anything untill the
                    # Next itteration, so store the value
                    if qubit1 == 1:
                        firstGate = mainGate
                    else:
                        firstGate = identity
                elif num == 2:
                    # If its the second itteration
                    if qubit1 == 2:
                        newMatrix = np.kron(firstGate, mainGate)
                    else:
                        newMatrix = np.kron(firstGate, identity)
                else:
                    if qubit1 == num:
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

    def applyGate(self, gate, qubit1, qubit2=-1):
        if self.measured:
            raise ValueError('Cannot Apply Gate to a Measured Quantum Register')
        else:
            if gate == 'CNOT':
                gateMatrix = gates.generateGate(
                    gate, self.numQubits, qubit1, qubit2)
                self.amplitudes = np.dot(self.amplitudes, gateMatrix)
            else:
                # Qubit 1 is the target
                gateMatrix = gates.generateGate(gate, self.numQubits, qubit1)
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
