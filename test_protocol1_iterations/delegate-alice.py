from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit
from parameters import N, L


#Here, we want to teleport a simple oracle
'''def gate(qubits):
        [qb.H() for qb in qubits]
        qubits[0].cphase(qubits[1])
        [qb.H() for qb in qubits]

        #Active low cphase
        [qb.X() for qb in qubits]
        qubits[0].cphase(qubits[1])
        [qb.X() for qb in qubits]

        [qb.H() for qb in qubits]

def gate_dag(qubits):
        gate(qubits)'''

def gate(qubits):
        [qb.Z() for qb in qubits]

def gate_dag(qubits):
        gate(qubits)
        


def main():

    with CQCConnection("Alice") as alice:
  
        for l in range(L):

                qubits = [qubit(alice) for i in range(N)]

                #Maximal superposition state
                [qb.H() for qb in qubits]

                if l==0:
                        gate(qubits)

                else:
                        #apply gate with correcting terms
                        gate_dag(qubits)
                        for i in range(N):
                                if previous_measurements[i]==1:
                                        qubits[i].X()
                        gate(qubits)
                        for i in range(N):
                                if previous_measurements[i]==1:
                                        qubits[i].X()



                print("sending qubits")
                for qb in qubits:
                        alice.sendQubit(qb, "Bob")


                #Receive Bob measurements
                previous_measurements = []
                for i in range(N):
                        previous_measurements.append(int(alice.recvClassical()))

                print(previous_measurements)

                print("Alice: Iteration", l, "done")


        print("Alice done")

main()