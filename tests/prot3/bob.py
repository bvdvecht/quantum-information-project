from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from bqc.prot3 import protocol3_recv
from bqc.prot3simplified import protocol3_recv_v2


def main():
    with CQCConnection("Bob") as bob:

        N = 2 #Number of qubits
        M = 2 #Number of sub-qubits : Must be a divider of N
        P = int(N/M)
        L = 3 #Number of steps for the protocol2

        R = []

        # receive J from Alice
        print("Bob: receive J")
        J = int.from_bytes(bob.recvClassical(close_after=True, timout=100), byteorder='big')
        print('J = ',J)

        protocol3_recv(bob, J, N, M, P, L, R)
        #protocol3_recv_v2(bob, J, M, M, 1, L, R)

        print("Bob done")
        
        


main()
exit()