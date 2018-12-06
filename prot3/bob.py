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
    return [ qb.measure(inplace=True) for qb in R ]


def protocol2_recv(bob, m, p, l, R):

    subR = R[p*m:(p+1)*m]

    for i in range(l):
        Rprime = recv_D_Plus(bob, m)
        measurements = teleport_proc(bob, m, subR, Rprime)
        for j in range(m):
            print("bob: send measurement")
            bob.sendClassical("Alice", measurements[j], close_after=True)
            print("bob: measurement sent")

        subR, Rprime = Rprime, subR

        print("Bob iteration", i, "done")

    tempR = R[0:p*m]
    tempR.extend(subR)
    tempR.extend(R[(p+1)*m:-1])
    R = tempR

    [qb.release for qb in Rprime]


def main():
    with CQCConnection("Bob") as bob:

        N = 2 #Number of qubits
        M = 2 #Number of sub-qubits : Must be a divider of N
        P = int(N/M)
        L = 1 #Number of steps for the protocol2

        R = []

        # receive initial psi from Alice
        for i in range(N):
            print("bob: receiving psi qubit")
            R.append(bob.recvQubit())
            print("bob: psi qubit received")

        # receive J from Alice
        print("Bob: receive J")
        J = int.from_bytes(bob.recvClassical(close_after=True, timout=10), byteorder='big')
        print('J = ',J)

        #Receives J=1 step qubits
        R = recv_D_Plus(bob, N)



        for j in range(1, J):

            #if j is odd, apply CZ
            if not((j+1)%2 == 0):

                [R[i].cphase(R[i+1]) for i in range(N-1)]

            #Bob applies H
            [R[i].H() for i in range(N)]


            for p in range(P):

                #Wait for alice to be ready and avoid timeout
                print("Bob: waiting for alice for p =", p)
                flag = bob.recvClassical(close_after=True, timout=10)

                #Engage protocol 2
                protocol2_recv(bob, M, p, L, R)


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