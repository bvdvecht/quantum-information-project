from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from bqc.prot3 import protocol3_recv


def main():
    with CQCConnection("Bob") as bob:

        N = 3 #Number of qubits
        M = 3 #Number of sub-qubits : Must be a divider of N
        P = int(N/M)
        L = 3 #Number of steps for protocol2

        R = []

        # receive J from Alice
        print("Bob: receive J")
        J = int.from_bytes(bob.recvClassical(close_after=True, timout=10), byteorder='big')
        print('J =', J)

        protocol3_recv(bob, J=J, N=N, M=M, L=L, R=R, P=P)

        print("Bob done")
        
        


main()