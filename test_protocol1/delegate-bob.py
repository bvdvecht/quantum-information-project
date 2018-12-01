from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

def main():
    with CQCConnection("Bob") as bob:
        
        N = 2

        #Register of alices qubits
        Rprime = []

        #Bob register
        R = [qubit(bob) for i in range(N)]

        #Receive D|+> of Alice
        for i in range(N):
                Rprime.append(bob.recvQubit())

        #Teleportation procedure
        # 1) Cnots
        [Rprime[i].cnot(R[i]) for i in range(N)]

        # 2) measure R, keep qubit !
        measurements = [qb.measure(inplace=True) for qb in R]

        # 3) Swap
        R, Rprime = Rprime, R
        
        # Note: in the iterated version, set measurement outcomes to alice, she must construc D_l+1 for the next gate.



        #At the end, Bob has X'D|psi> in his register where X' = product(X'_l). In this example there is only one iteration so l=1
        #To recover D|psi>, just apply X'

        for i in range(N):
                if measurements[i]==0:
                        R[i].X()

        print("Bob done")
        

        print("Bob output: ", R[0].measure(), R[1].measure())



        #Send a flag to alice to say that the transaction is done
        #bob.sendClassical("Alice", 0)

main()