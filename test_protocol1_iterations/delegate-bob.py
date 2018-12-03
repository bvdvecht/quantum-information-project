from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit
from parameters import N, L


def main():
    with CQCConnection("Bob") as bob:

        #Bob register
        R = [qubit(bob) for i in range(N)]
        [qb.H() for qb in R]

        #Bob measurements
        cumulated_measurements = [0 for i in range(N)]

        #Alice qubits[]
        Rprime = []


        for l in range(L):

                #Receive D|+> of Alice 

                Rprime = []

                for i in range(N):
                        print("receiving qubit")
                        Rprime.append(bob.recvQubit())
                        print("qubit received")

                #Teleportation procedure
                # 1) Cnots
                [Rprime[i].cnot(R[i]) for i in range(N)]

                # 2) measure R, without releasing the qubit
                measurements = [qb.measure(inplace=True) for qb in R]

                # 3) Swap
                R, Rprime = Rprime, R

                #Releasing Rprime qubits
                [qb.release() for qb in Rprime]
                
                # 4) send measurements to Alice
                for i in range(N):
                        bob.sendClassical("Alice", measurements[i])

                # XOR measurements to cumulated_measurements for step
                cumulated_measurements = [(cumulated_measurements[i] + measurements[i])%2 for i in range(N)]

                print("Bob iteration", l, "done")



        #At the end, Bob has X'D|psi> in his register where X' = product(X'_l).
        #To recover D|psi>, just apply X'

        for i in range(N):
                if cumulated_measurements[i]==1:
                        R[i].X()

        print("Bob done")
        
        [qb.H() for qb in R]
        print("Bob output: ", R[0].measure(), R[1].measure())

main()