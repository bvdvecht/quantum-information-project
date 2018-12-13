from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from bqc.prot2 import protocol2_recv, recv_D_Plus


def main():
    with CQCConnection("Bob") as bob:

        N = 2 #Number of qubits
        M = 2 #Number of sub-qubits : Must be a divider of N
        P = int(N/M)
        L = 1 #Number of steps for the protocol2

        R = []

        # receive J from Alice
        print("Bob: receive J")
        J = int.from_bytes(bob.recvClassical(close_after=True, timout=10), byteorder='big')
        print('J = ',J)

        #Receives J=1 step qubits
        R = recv_D_Plus(bob, N)



        for j in range(2, J+1):

            #if j is odd, apply CZ
            if (j % 2) != 0:
                [R[i].cphase(R[i+1]) for i in range(N-1)]

            #Bob applies H
            [R[i].H() for i in range(N)]


            for p in range(P):

                #Wait for alice to be ready and avoid timeout
                print("Bob: waiting for alice for p =", p)
                flag = bob.recvClassical(close_after=True, timout=10)

                #Engage protocol 2
                R = protocol2_recv(bob, M, p, L, R)


            print("Bob depth", j, "done")


        #Bob measures in X basis
        for qb in R:
            qb.H()
            meas = qb.measure(inplace=True)
            qb.H()
            bob.sendClassical("Alice", meas, close_after=True)

            
        # send result to Alice
        '''for qb in R:
            bob.sendQubit(qb, "Alice")'''

        print("Bob done")
        
        


main()