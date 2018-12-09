from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

def recv_D_Plus(bob, m):
    Rprime = []
    for i in range(m):
        print("bob recv_D_Plus: receive qubit")
        Rprime.append(bob.recvQubit())
        print("bob recv_D_Plus: qubit received")

    return Rprime

def teleport_proc(bob, m, R, Rprime):
    [ Rprime[i].cnot(R[i]) for i in range(m) ]
    return [ qb.measure(inplace=False) for qb in R ]


def main():
    with CQCConnection("Bob") as bob:
        m = 2
        l = 3

        R = []

        # receive initial psi from Alice
        for i in range(m):
            print("bob: receiving psi qubit")
            R.append(bob.recvQubit())
            print("bob: psi qubit received")

        

        for i in range(l):
            Rprime = recv_D_Plus(bob, m)
            measurements = teleport_proc(bob, m, R, Rprime)
            for j in range(m):
                print("bob: send measurement")
                bob.sendClassical("Alice", measurements[j], close_after=True)
                print("bob: measurement sent")

            R, Rprime = Rprime, R

            print("Bob iteration", i, "done")

            
        # send result to Alice
        for qb in R:
            bob.sendQubit(qb, "Alice")

        print("Bob done")
        
        


main()