from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from bqc.gates import PrimitiveGate, CompositeGate, TensorGate, EntangleGate
from bqc.prot3_v9000 import compute_target_gate
from bqc.prot3_v9000 import protocol3


def main():
    with CQCConnection("Alice") as alice:  

        J = 3 #Depth
        N = 3 #Number of qubits
        M = 1 #Number of sub-qubits : Must be a divider of N
        P = int(N/M)
        L = 3 #Number of steps for the protocol2

        # Definition of the target gates for all j and all p (J rows, P columns), except the first row which must be a tensor(N) gate
        '''
        D_gates = [ TensorGate(['I']),\
                    [ TensorGate(['I']) ],\
                    [ TensorGate(['I']) ],\
                    [ TensorGate(['I']) ],\
                    [ TensorGate(['I']) ] ] 

        
        D_gates = [ TensorGate(['I', 'I']),\
                    [ TensorGate(['I', 'I']) ],\
                    [ TensorGate(['I', 'I']) ],\
                    [ TensorGate(['I', 'I']) ],\
                    [ TensorGate(['I', 'I']) ] ] 

               
        D_gates = [ TensorGate(['I', 'Z']),\
                    [ TensorGate(['I']), TensorGate(['I']) ],\
                    [ TensorGate(['Z']), TensorGate(['I']) ],\
                    [ TensorGate(['I']), TensorGate(['I']) ],\
                    [ TensorGate(['I']), TensorGate(['I']) ] ] 
        

        '''
        # first row is a single (n-qubit) gate
        # other rows are p m-qubit gates
        D_gates = [ TensorGate(['I', 'I', 'Z']),\
                    [ TensorGate(['Z']), TensorGate(['I']), TensorGate(['I']) ],\
                    [ TensorGate(['I']), TensorGate(['Z']), TensorGate(['I']) ],\
                    [ TensorGate(['I']), TensorGate(['I']), TensorGate(['I']) ],\
                    [ TensorGate(['I']), TensorGate(['I']), TensorGate(['I']) ] ] 
        # should give result 0 1 1

        result = protocol3(alice, J=J, N=N, M=M, L=L, D_gates=D_gates, P=P)

        print('\nRESULT:', result)

main()