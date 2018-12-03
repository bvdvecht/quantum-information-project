from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

def main():
    with CQCConnection("Alice") as alice:
        
        N = 1

        #Alice qubits
        qubits = [qubit(alice) for i in range(N)]

        #Maximal superposition state
        [qb.H() for qb in qubits]



        #Applying the desired gate: here a simple quantum oracle

        '''[qb.H() for qb in qubits]
        qubits[0].cphase(qubits[1])
        [qb.H() for qb in qubits]

        #Active low cphase
        [qb.X() for qb in qubits]
        qubits[0].cphase(qubits[1])
        [qb.X() for qb in qubits]

        [qb.H() for qb in qubits]'''

        # Z gate
        [qb.Z() for qb in qubits]


        [alice.sendQubit(qb, "Bob") for qb in qubits]

        print("Alice done")
        print("blablabl")

        #Holds alice while bob has not finished, timeout 10sec
        #flag = alice.recvClassical()
        #print("Connection closed")


main()