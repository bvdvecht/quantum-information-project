from SimulaQron.cqc.pythonLib.cqc import CQCConnection
from bqc.prot1 import protocol1_recv

def main():
    with CQCConnection("Bob") as bob:
        m = 2
        l = 3

        R = []

        # receive initial psi from Alice
        for i in range(m):
            #print("bob: receiving psi qubit")
            R.append(bob.recvQubit())
            #print("bob: psi qubit received")

        print('initial state of Bob:')
        for qb in R:
            qb.Y()
        print('\n')

        R = protocol1_recv(bob, m, 0, l, R)
            
        # send result to Alice
        for qb in R:
            bob.sendQubit(qb, "Alice")

        print("Bob done")


main()