from SimulaQron.cqc.pythonLib.cqc import CQCConnection

from bqc.gates import TensorGate, RotZGate, ROT_PI_4, ROT_PI_2, EntangleGate
from bqc.gates import SimpleGate as SG
from bqc.prot3 import protocol3_send


def main():
    with CQCConnection("Alice") as alice:

        # Deutsch-Jozsa for f: {0,1}^2 -> {0,1}  (2 bits to 1 bit)
        # with f(x, y) = x + y (mod 2)
        #
        # see the report for the exact circuit

        D_gates = [ TensorGate([SG('I'), RotZGate(-ROT_PI_2), SG('Z')]),
                    [ TensorGate([SG('I'), RotZGate(-ROT_PI_4), SG('I')]) ],
                    [ TensorGate([SG('I'), SG('I'), SG('I')]) ],
                    [ TensorGate([SG('I'), SG('I'), SG('I')]) ],
                    [ TensorGate([SG('I'), SG('Z'), SG('I')]) ],
                    [ TensorGate([SG('I'), RotZGate(ROT_PI_4), SG('I')]) ],
                    [ TensorGate([SG('I'), SG('I'), SG('I')]) ],
                    [ TensorGate([SG('I'), SG('I'), SG('I')]) ],
                    [ TensorGate([SG('I'), RotZGate(ROT_PI_2), SG('I')]) ],
                    [ TensorGate([SG('I'), SG('I'), SG('I')])],
                    # until here: H on second qubit, X on third qubit
                    # CPHASE on qubits 1,2,3
                    [ TensorGate([EntangleGate('CPHASE'), None, SG('I')])],
                    [ TensorGate([SG('I'), SG('I'), SG('I')])],
                    # CPHASE on qubits 1,2,3
                    [ TensorGate([SG('I'), RotZGate(-ROT_PI_2), SG('I')]) ],
                    [ TensorGate([SG('I'), RotZGate(-ROT_PI_4), SG('I')]) ],
                    [ TensorGate([SG('I'), SG('I'), SG('I')]) ],
                    [ TensorGate([SG('I'), SG('I'), SG('I')]) ],
                    [ TensorGate([SG('I'), SG('Z'), SG('I')]) ],
                    [ TensorGate([SG('I'), RotZGate(ROT_PI_4), SG('I')]) ],
                    [ TensorGate([SG('I'), SG('I'), SG('I')]) ],
                    [ TensorGate([SG('I'), SG('I'), SG('I')]) ],
                    [ TensorGate([SG('I'), RotZGate(ROT_PI_2), SG('I')]) ],
                    [ TensorGate([SG('I'), SG('I'), SG('I')]) ],
                    # until here: H on second qubit
                    [ TensorGate([SG('I'), SG('I'), SG('I')]) ], # to undo CPHASE
                    [ TensorGate([SG('I'), SG('I'), SG('I')]) ], # to undo CPHASE
                    [ TensorGate([SG('I'), SG('I'), SG('I')]) ] ] # for extra layer of H


        # J = 22  # Depth
        J = len(D_gates)
        N = 3  # Number of qubits
        M = 3  # Number of sub-qubits : Must be a divider of N
        P = int(N / M)
        L = 3  # Number of steps for protocol2

        result = protocol3_send(alice, J=J, N=N, M=M, L=L, D_gates=D_gates, P=P, debug=True)

        print('\nRESULT:', result)
        #type = 'balanced' if result[0] == 1 else 'constant'
        #int('--> f is', type)

main()
