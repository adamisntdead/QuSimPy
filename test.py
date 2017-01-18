import unittest

import QuSim

###########################################
#                Cases                    #
###########################################
# Pauli-X Gate
X = QuSim.QuantumRegister(1)
X.applyGate('X', 1)

# Multiple qubits
Multi = QuSim.QuantumRegister(5)
Multi.applyGate('X', 4)

# CNOT Gates
CNOT1 = QuSim.QuantumRegister(10)
CNOT1.applyGate('CNOT', 3, 7)

CNOT2 = QuSim.QuantumRegister(10)
CNOT2.applyGate('X', 3)
CNOT2.applyGate('CNOT', 3, 7)

CNOT3 = QuSim.QuantumRegister(9)
CNOT3.applyGate('X', 3)
CNOT3.applyGate('X', 7)
CNOT3.applyGate('CNOT', 3, 7)

###########################################
#                Tests                    #
###########################################


class QuSimTests(unittest.TestCase):
    def testXGate(self):
        self.assertEqual(X.measure(), '1')

    def testMultipleQubits(self):
        self.assertEqual(Multi.measure(), '00010')

    def testCNOT(self):
        self.assertEqual(CNOT1.measure(), '0000000000')
        self.assertEqual(CNOT2.measure(), '0010001000')
        self.assertEqual(CNOT3.measure(), '001000000')

    def testRemeasure(self):
        self.assertEqual(CNOT1.measure(), '0000000000')
        self.assertEqual(CNOT2.measure(), '0010001000')
        self.assertEqual(CNOT3.measure(), '001000000')

    def testReapplyGate(self):
        with self.assertRaises(ValueError):
            CNOT1.applyGate('X', 4)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
