from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

def recv_D_Plus(bob, m):
    Rprime = []
    for i in range(m):
        print("receiving qubit")
        Rprime.append(bob.recvQubit())
        print("qubit received")

    return Rprime

def teleport_proc(bob, m, R, Rprime):
    [ Rprime[i].cnot(R[i]) for i in range(m) ]
    return [ qb.measure(inplace=True) for qb in R ]


def main():
    with CQCConnection("Bob") as bob:
        m = 2
        l = 2

        R = []

        # receive initial psi from Alice
        for i in range(m):
            print("receiving qubit")
            R.append(bob.recvQubit())
            print("qubit received")

        

        print('prepared initial psi')

        for i in range(l):
            Rprime = recv_D_Plus(bob, m)
            measurements = teleport_proc(bob, m, R, Rprime)
            # for i in range(m):
            #     bob.sendClassical("Alice", measurements[i])

            R, Rprime = Rprime, R

            print("Bob iteration", i, "done")

            
        # send result to Alice
        for qb in R:
            bob.sendQubit(qb, "Alice")

        print("Bob done")
        
        


main()