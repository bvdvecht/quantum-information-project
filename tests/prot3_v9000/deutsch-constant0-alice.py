from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from bqc.gates import PrimitiveGate, CompositeGate, TensorGate, EntangleGate
from bqc.prot3_v9000 import compute_target_gate
from bqc.prot3_v9000 import protocol3


def main():
    with CQCConnection("Alice") as alice:  

        # Deutsch-Jozsa for f: {0,1} -> {0,1}  (1 bit to 1 bit)
        # with f(0) = f(1) = 0, i.e. U_f = I tensor I
        #
        # circuit:
        # 0 - I - H - |-----| - H - measure in std basis
        #             | U_f |
        # 0 - X - H - |-----| - H
        #
        # let Bob compute this blindly using the following circuit:
        # 0 - . - H -|I|- H -|I|- . - H -|I|
        #     |      | |     | |  |      | |
        # 0 - . - H -|Z|- H -|I|- . - H -|I|
        #             D1      D2          D3
        #         <   I X  >         <H> <U_f>
        #
        # measuring the output of Bob's circuit in the X basis implicitly applies the last H
        # gates needed for the Deutsch-Jozsa algorithm

        J = 3  # Depth
        N = 2  # Number of qubits
        M = 2  # Number of sub-qubits : Must be a divider of N
        P = int(N / M)
        L = 3  # Number of steps for protocol2

        D_gates = [ TensorGate(['I', 'Z']),\
                    [ TensorGate(['I', 'I']) ],\
                    [ TensorGate(['I', 'I']) ], ]


        result = protocol3(alice, J=J, N=N, M=M, L=L, D_gates=D_gates, P=P)

        print('\nRESULT:', result)

main()