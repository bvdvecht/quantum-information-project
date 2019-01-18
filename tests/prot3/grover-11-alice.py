from SimulaQron.cqc.pythonLib.cqc import CQCConnection

from bqc.gates import TensorGate, EntangleGate
from bqc.gates import SimpleGate as SG
from bqc.prot3 import protocol3


def main():
    with CQCConnection("Alice") as alice:  

        # Grover for searching bit string '11' in set of 2-bit strings
        #
        # circuit:
        # 0 - H - |-----| - H - X - . - X - H - measure in std basis
        #         | U_f |           |
        # 0 - H - |-----| - H - X - . - X - H
        #                      inv about mean

        D_gates = [
            EntangleGate('CPHASE'), # = U_f
            [TensorGate([SG('I'), SG('I')])], # filler
            [TensorGate([SG('I'), SG('I')])], # to undo Bob's CPHASE
            [TensorGate([SG('I'), SG('I')])], # to undo Bob's CPHASE
            [TensorGate([SG('Z'), SG('Z')])], # X for active-low CPHASE
            [TensorGate([SG('I'), SG('I')])], # filler
            # Bob does CPHASE here as part of inversion about mean
            [TensorGate([SG('Z'), SG('Z')])], # X for active-low CPHASE
            [TensorGate([SG('I'), SG('I')])] # filler
        ]

        J = len(D_gates) # Depth
        # J = 6  # Depth
        N = 2  # Number of qubits
        M = 2  # Number of sub-qubits : Must be a divider of N
        P = int(N / M)
        L = 3  # Number of steps for protocol2

        result = protocol3(alice, J=J, N=N, M=M, L=L, D_gates=D_gates, P=P)

        print('\nRESULT:', result)

main()
