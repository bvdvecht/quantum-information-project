from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from bqc.gates import PrimitiveGate, CompositeGate, TensorGate, EntangleGate
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
        # 0 - . - H -|I|- H -|.|- . - H -|Z|- H - |I| - MEASURE in x basis
        #     |      | |     |||  |      | |     
        # 0 - . - H -|Z|- H -|.|- . - H -|I|- H - |I| 
        #             D1      D2          D3  
        #         <   I X  >  <Cphase>        
        #
        # measuring the output of Bob's circuit in the X basis implicitly applies the last H
        # gates needed for the Deutsch-Jozsa algorithm

        J = 4  # Depth
        N = 2  # Number of qubits
        M = 2  # Number of sub-qubits : Must be a divider of N
        P = int(N / M)
        L = 3  # Number of steps for protocol2

        D_gates = [ TensorGate(['I', 'Z']),\
                    [ EntangleGate('CPHASE') ],\
                    [ TensorGate(['Z', 'I']) ],\
                    [ TensorGate(['I', 'I'])] ]


        result = protocol3(alice, J=J, N=N, M=M, L=L, D_gates=D_gates, P=P)

        print('\nRESULT:', result)

main()