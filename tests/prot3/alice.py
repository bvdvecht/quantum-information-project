from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from bqc.gates import PrimitiveGate, CompositeGate, TensorGate, EntangleGate
from bqc.prot3 import compute_target_gate
from bqc.prot3 import protocol3
from bqc.prot3simplified import protocol3_v2


def main():
    with CQCConnection("Alice") as alice:  

        J = 3 #Depth
        N = 2 #Number of qubits
        M = 2 #Number of sub-qubits : Must be a divider of N
        P = int(N/M)
        L = 3 #Number of steps for the protocol2

        # Definition of the target gates for all j and all p (J rows, P columns), except the first row which must be a tensor(N) gate
        '''D_gates = [ [TensorGate(['Z', 'I'])],\
                    [TensorGate(['I', 'Z'])],\
                    [TensorGate(['Z', 'Z'])] ] # should give 01 as result'''

        D_gates = [ [TensorGate(['Z', 'I'])],\
                    [TensorGate(['I', 'Z'])],\
                    [TensorGate(['I', 'Z'])] ] # should give 11 as result

        #The final gate is (D4 H D3 H D2 H D1 H)

        result = protocol3(alice, J, N, M, P, L, D_gates, no_encrypt=False)
        #result = protocol3_v2(alice, J, M, M, 1, L, D_gates, no_encrypt=False)

        print("Alice: output bits: ", result)

main()
exit()