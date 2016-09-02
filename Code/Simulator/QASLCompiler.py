#!/usr/bin/python
import argparse
import os
import sys

##############################################
import ply.lex as lex

# Tokens List
tokens = [
    'NAME',
    'NUMBER',
    'PARAMOPEN',
    'PARAMCLOSE',
    'BREAK'
]

# Token Definitions
t_PARAMOPEN = r'\['
t_PARAMCLOSE = r'\]'
t_BREAK = r'\n'
t_ignore = r' '


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = 'NAME'
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_error(t):
    # For Illegal Charachters
    t.lexer.skip(1)

lexer = lex.lex()


def parse(input):
    # List of Gates in the simulator, used for error checking:
    Gates = ['X', 'Y', 'Z', 'H', 'ID', 'S', 'SDAGGER', 'T', 'TDAGGER', 'CNOT']

    # Lex The Input
    lexer.input(input)

    # This will hold the stack, which will be sent to
    # The Code Generator
    instructionStack = []

    currentStack = []
    currentParams = 0
    for tok in lexer:
        curLen = len(currentStack)

        # If theres a new line, figure out if its imporant
        if tok.type == 'BREAK':
            if curLen == 0:
                pass
            else:
                instructionStack.append(currentStack)
                currentStack = []
                currentParams = 0
        elif tok.type == 'NAME':
            if (tok.value.upper() == 'MEASURE'):
                if curLen != 0:
                    raise ValueError('Misuse of Keyword "MEASURE"')
                else:
                    currentStack.append('MEASURE')
            # Check for misuse of QUREG
            elif (curLen != 0 and tok.value.lower() == 'qureg'):
                raise ValueError('Misuse of Keyword "QUREG"', tok.lexpos)
            # Push the new quantum register instruction to the current stack
            elif tok.value.lower() == 'qureg':
                currentStack.append('QUREG')
            else:
                currentStack.append(tok.value)

        elif tok.type == 'NUMBER':
            if (currentParams >= 2 or currentStack[0] == 'MEASURE'):
                raise ValueError('Too Many Parameters Given On Input')
            elif (curLen != 0):
                currentParams = currentParams + 1
                currentStack.append(tok.value)

    # Go Through the instructionStack, and make the first string capitolized.
    for i in range(0, len(instructionStack)):
        instructionStack[i][0] = instructionStack[i][0].upper()

    # Return Our Now Parsed InstructionStack
    return instructionStack


def generate(input):
    instructionStack = parse(input)

    CodeString = 'import QuSim\n\n'

    for instruction in instructionStack:
        newCode = ''
        if instruction[0] == 'QUREG':
            newCode = instruction[
                1] + ' = QuSim.QuantumRegister(' + str(instruction[2]) + ')'

        elif instruction[0] == 'MEASURE':
            newCode = 'print(' + instruction[1] + '.measure())'

        else:
            if len(instruction) == 4:
                newCode = instruction[1] + '.applyGate("' + instruction[0] + '", ' + str(
                    instruction[2]) + ', ' + str(instruction[3]) + ')'
            else:
                newCode = instruction[
                    1] + '.applyGate("' + instruction[0] + '", ' + str(instruction[2]) + ')'

        CodeString = CodeString + newCode + '\n'

    return CodeString

#############################################

# Start Parsing Arguments
argParser = argparse.ArgumentParser()
# Add argument for the source file
argParser.add_argument("source", help="The Source File in QASL")

# Add Argument
argParser.add_argument(
    "--output", help="Output The Compiled File (As Python)", action="store_true")
args = argParser.parse_args()


####################################################
#                 Start Compiling                  #
####################################################
sourceFile = open(args.source, 'r')

compiledCode = generate(sourceFile.read())

if args.output:
    file = open('output.py', 'w+')
    file.write(compiledCode)
    file.close()
else:
    exec(compiledCode)
