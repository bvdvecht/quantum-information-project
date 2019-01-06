from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from bqc.prot2 import protocol2_recv

def main():
    with CQCConnection("Bob") as bob:
        m = 2
        l = 1
        p = 1

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

        R = protocol2_recv(bob, m, p, l, R, debug=True)
            
        # send result to Alice
        for qb in R:
            bob.sendQubit(qb, "Alice")

        print("Bob done")
        
        
main()