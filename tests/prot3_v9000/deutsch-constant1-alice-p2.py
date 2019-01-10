from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

# from bqc.gates import PrimitiveGate, CompositeGate, TensorGate, EntangleGate
from bqc.gates2 import TensorGate
from bqc.gates2 import SimpleGate as SG
from bqc.prot3_v9000 import compute_target_gate
from bqc.prot3_v9000 import protocol3


def main():
    with CQCConnection("Alice") as alice:  

        # Deutsch-Jozsa for f: {0,1} -> {0,1}  (1 bit to 1 bit)
        # with f(0) = f(1) = 1, i.e. U_f = I tensor X
        #
        # circuit:
        # 0 - I - H - |-----| - H - measure in std basis
        #             | U_f |
        # 0 - X - H - |-----| - H
        #
        # let Bob compute this blindly using the following circuit:
        # 0 - . - H -|I|- H -|I|- . - H -|I|- H -|I|- . - H -|I|
        #     |      | |     | |  |      | |     | |  |      | |
        # 0 - . - H -|Z|- H -|I|- . - H -|I|- H -|Z|- . - H -|I|
        #             D1      D2          D3      D4          D5
        #         <   I X  >         <H>     <  U_f = I X  >
        #
        # measuring the output of Bob's circuit in the X basis implicitly applies the last H
        # gates needed for the Deutsch-Jozsa algorithm

        J = 5  # Depth
        N = 2  # Number of qubits
        M = 1  # Number of sub-qubits : Must be a divider of N
        P = int(N / M)
        L = 3  # Number of steps for protocol2

        D_gates = [ TensorGate([SG('I'), SG('Z')]),\
                    [ TensorGate([SG('I')]), TensorGate([SG('I')]) ],\
                    [ TensorGate([SG('I')]), TensorGate([SG('I')]) ], \
                    [ TensorGate([SG('I')]), TensorGate([SG('Z')]) ], \
                    [ TensorGate([SG('I')]), TensorGate([SG('I')]) ], ]


        result = protocol3(alice, J=J, N=N, M=M, L=L, D_gates=D_gates, P=P)

        print('\nRESULT:', result)
        type = 'balanced' if result[0] == 1 else 'constant'
        print('--> f is', type)

main()