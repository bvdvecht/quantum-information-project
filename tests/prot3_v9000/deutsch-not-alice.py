from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from bqc.gates import PrimitiveGate, CompositeGate, TensorGate, EntangleGate, CustomDiagonalGate
from bqc.prot3_v9000 import compute_target_gate
from bqc.prot3_v9000 import protocol3


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

        J = 8  # Depth
        N = 2  # Number of qubits
        M = 2  # Number of sub-qubits : Must be a divider of N
        P = int(N / M)
        L = 3  # Number of steps for protocol2

        D_gates = [ TensorGate([CustomDiagonalGate([0, 32]), 'Z']),\
                        [ TensorGate([CustomDiagonalGate([-16, 16]), 'I']) ],\
                        [ TensorGate(['Z', 'I']) ],\
                        [ TensorGate([CustomDiagonalGate([16, -16]), 'I']) ],\
                        [ TensorGate([CustomDiagonalGate([0, -32]), 'I']) ],\
                        [ EntangleGate('CPHASE') ],\
                        [ TensorGate(['Z', 'I']) ],\
                        [ TensorGate(['I', 'I'])] ]


        result = protocol3(alice, J=J, N=N, M=M, L=L, D_gates=D_gates, P=P)

        print('\nRESULT:', result)

main()


'''
Circuit can be found on
https://algassert.com/quirk#circuit={%22cols%22:[[%22H%22,%22H%22],[%22~ega%22,%22Z%22],[%22H%22,%22H%22],[%22~dqmn%22],[%22H%22,%22H%22],[%22Z%22],[%22H%22,%22H%22],[%22~bel6%22],[%22H%22,%22H%22],[%22~uals%22],[%22H%22,%22H%22],[%22%E2%80%A2%22,%22Z%22],[%22H%22,%22H%22],[%22Z%22]],%22gates%22:[{%22id%22:%22~ega%22,%22name%22:%221%22,%22matrix%22:%22{{%E2%88%9A%C2%BD+%E2%88%9A%C2%BDi,0},{0,%E2%88%9A%C2%BD-%E2%88%9A%C2%BDi}}%22},{%22id%22:%22~5i51%22,%22name%22:%222%22,%22matrix%22:%22{{1,0},{0,%E2%88%9A%C2%BD-%E2%88%9A%C2%BDi}}%22},{%22id%22:%22~3gu0%22,%22name%22:%223%22,%22matrix%22:%22{{1,0},{0,%E2%88%9A%C2%BD+%E2%88%9A%C2%BDi}}%22},{%22id%22:%22~uals%22,%22name%22:%224%22,%22matrix%22:%22{{%E2%88%9A%C2%BD-%E2%88%9A%C2%BDi,0},{0,%E2%88%9A%C2%BD+%E2%88%9A%C2%BDi}}%22},{%22id%22:%22~fvjr%22,%22name%22:%222b%22,%22matrix%22:%22{{0.9238795-0.3826834i,0},{0,0.9238795+0.3826834i}}%22},{%22id%22:%22~dqmn%22,%22name%22:%222B%22,%22matrix%22:%22{{0.9238795+0.3826834i,0},{0,0.9238795-0.3826834i}}%22},{%22id%22:%22~bel6%22,%22name%22:%223B%22,%22matrix%22:%22{{0.9238795-0.3826834i,0},{0,0.9238795+0.3826834i}}%22}]}
'''