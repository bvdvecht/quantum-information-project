from SimulaQron.cqc.pythonLib.cqc import CQCConnection

from bqc.gates import TensorGate, RotZGate, ROT_PI_4, ROT_PI_2
from bqc.gates import SimpleGate as SG
from bqc.prot3 import protocol3_send


def main():
    with CQCConnection("Alice") as alice:  

        # Deutsch-Jozsa for f: {0,1} -> {0,1}  (1 bit to 1 bit)
        # with f(x) = not(x), i.e. U_f = active-low CNOT
        #
        # circuit:
        # 0 - I - H - |-----| - H - measure in std basis
        #             | U_f |
        # 0 - X - H - |-----| - H
        #          <active-low CNOT>
        #
        # let Bob compute this blindly using the following circuit:
        #
        # To see the circuit, checkout Deutch_not.JPG or link below  
        #
        # measuring the output of Bob's circuit in the X basis implicitly applies the last H
        # gates needed for the Deutsch-Jozsa algorithm

        J = 16 # Depth
        N = 2  # Number of qubits
        M = 1  # Number of sub-qubits : Must be a divider of N
        P = int(N / M)
        L = 3  # Number of steps for protocol2

        D_gates = [ TensorGate([RotZGate(-ROT_PI_2), SG('Z')]),\
                        [ TensorGate([RotZGate(-ROT_PI_4)]), TensorGate([SG('I')]) ],\
                        [ TensorGate([SG('I')]), TensorGate([SG('I')]) ], \
                        [ TensorGate([SG('I')]), TensorGate([SG('I')]) ], \
                        [ TensorGate([SG('Z')]), TensorGate([SG('I')]) ], \
                        [ TensorGate([RotZGate(ROT_PI_4)]), TensorGate([SG('I')]) ],\
                        [ TensorGate([SG('I')]), TensorGate([SG('I')]) ],\
                        [ TensorGate([SG('I')]), TensorGate([SG('I')]) ],\
                        [ TensorGate([RotZGate(ROT_PI_2)]), TensorGate([SG('I')]) ],\
                        [ TensorGate([SG('I')]), TensorGate([SG('I')])], \
                        # until here: H on first qubit, X on second qubit
                        [TensorGate([SG('I')]), TensorGate([SG('I')])], \
                        [TensorGate([SG('I')]), TensorGate([SG('I')])], \
                        [TensorGate([SG('Z')]), TensorGate([SG('I')])], \
                        [TensorGate([SG('I')]), TensorGate([SG('I')])], \
                        # cphase done here by Bob
                        [TensorGate([SG('Z')]), TensorGate([SG('I')])], \
                        [TensorGate([SG('I')]), TensorGate([SG('I')])] ]

        result = protocol3_send(alice, J=J, N=N, M=M, L=L, D_gates=D_gates, P=P)

        print('\nRESULT:', result)
        type = 'balanced' if result[0] == 1 else 'constant'
        print('--> f is', type)

main()


'''
Circuit can be found on
https://algassert.com/quirk#circuit={%22cols%22:[[%22H%22,%22H%22],[%22~ega%22,%22Z%22],[%22H%22,%22H%22],[%22~dqmn%22],[%22H%22,%22H%22],[%22Z%22],[%22H%22,%22H%22],[%22~bel6%22],[%22H%22,%22H%22],[%22~uals%22],[%22H%22,%22H%22],[%22%E2%80%A2%22,%22Z%22],[%22H%22,%22H%22],[%22Z%22]],%22gates%22:[{%22id%22:%22~ega%22,%22name%22:%221%22,%22matrix%22:%22{{%E2%88%9A%C2%BD+%E2%88%9A%C2%BDi,0},{0,%E2%88%9A%C2%BD-%E2%88%9A%C2%BDi}}%22},{%22id%22:%22~5i51%22,%22name%22:%222%22,%22matrix%22:%22{{1,0},{0,%E2%88%9A%C2%BD-%E2%88%9A%C2%BDi}}%22},{%22id%22:%22~3gu0%22,%22name%22:%223%22,%22matrix%22:%22{{1,0},{0,%E2%88%9A%C2%BD+%E2%88%9A%C2%BDi}}%22},{%22id%22:%22~uals%22,%22name%22:%224%22,%22matrix%22:%22{{%E2%88%9A%C2%BD-%E2%88%9A%C2%BDi,0},{0,%E2%88%9A%C2%BD+%E2%88%9A%C2%BDi}}%22},{%22id%22:%22~fvjr%22,%22name%22:%222b%22,%22matrix%22:%22{{0.9238795-0.3826834i,0},{0,0.9238795+0.3826834i}}%22},{%22id%22:%22~dqmn%22,%22name%22:%222B%22,%22matrix%22:%22{{0.9238795+0.3826834i,0},{0,0.9238795-0.3826834i}}%22},{%22id%22:%22~bel6%22,%22name%22:%223B%22,%22matrix%22:%22{{0.9238795-0.3826834i,0},{0,0.9238795+0.3826834i}}%22}]}
'''