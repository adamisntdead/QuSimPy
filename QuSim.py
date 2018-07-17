from functools import reduce
import numpy as np

class gates:
    i = np.complex(0, 1)

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
        'H': np.multiply(1. / np.sqrt(2), np.matrix([
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
            [0, np.e**(i * np.pi / 4.)]
        ]),
        'TDagger': np.matrix([
            [1, 0],
            [0, np.e**(i * np.pi / 4.)]
        ]).conjugate().transpose()
    }

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
            gateOrder = (mainGate if i == qubit1 else identity
                         for i in range(1, numQubits + 1))
            return reduce(np.kron, gateOrder)


class QuantumRegister:

    def __init__(self, numQubits):
        self.numQubits = numQubits

        # The number of amplitudes needed is 2^n, where N is the 
        # number of qubits, So start with a vector of zeros.
        self.amplitudes = np.zeros(2**numQubits)
        # Set the probabilit of getting 0 when measured to 1
        self.amplitudes[0] = 1

        self.value = False

    def applyGate(self, gate, qubit1, qubit2=-1):
        if self.value:
            raise ValueError('Cannot Apply Gate to Measured Register')
        else:
            # Generate the gate matrix
            gateMatrix = gates.generateGate(
                gate, self.numQubits, qubit1, qubit2)
            # Calculate the new state vector by multiplying by the gate
            self.amplitudes = np.dot(self.amplitudes, gateMatrix)

    def measure(self):
        if self.value:
            return self.value
        else:
            # Get this list of probabilities, by squaring the absolute
            # value of the amplitudes
            self.probabilities = []
            for amp in np.nditer(self.amplitudes):
                probability = np.absolute(amp)**2
                self.probabilities.append(probability)

            # Now, we need to make a weighted random choice of all of the possible
            # output states (done with the range function)

            results = list(range(len(self.probabilities)))
            self.value = np.binary_repr(
                np.random.choice(results, p=self.probabilities),
                self.numQubits
            )
            return self.value

# And thats it!