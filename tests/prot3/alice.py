from random import randint
import time
import copy
from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from bqc.gates import PrimitiveGate, CompositeGate, TensorGate, EntangleGate
from bqc.prot2 import protocol2, send_D_Plus

def compute_target_gate(j, p, N, M, X_record, Z_record, D):

    chi = []
    zeta = []

    #The list is padded with two null rows at the beginning, and zeros at the left and right borders
    padded_X_record = [[0 for i in range(M+2)], [0 for i in range(M+2)]]
    for x in X_record:
        line = [0]
        line.extend(x)
        line.append(0)
        padded_X_record.append(line)

    #The list is padded with three null rows at the beginning, and zeros at the left and right borders
    padded_Z_record = [[0 for i in range(M+2)], [0 for i in range(M+2)], [0 for i in range(M+2)]]
    for z in Z_record:
        line = [0]
        line.extend(z)
        line.append(0)
        padded_Z_record.append(line)



    #if j even
    if (j+1)%2==0:
        
        #chi(j,k) = z(j-1, k)
        chi = [padded_Z_record[j+2][i+1] for i in range(p*N, (p+1)*N)]

        #zeta(j,k) = z(j-2, k) + x(j1, k) + sum_{-1,1}(z(j-3, k+i) + x(j-2, k+i))
        zeta = [ (padded_Z_record[j+1][i+1] + padded_X_record[j+1][i+1] \
         + padded_Z_record[j][i] + padded_X_record[j][i] + padded_Z_record[j][i+2] + padded_X_record[j][i+2]) %2 \
         for i in range(p*N, (p+1)*N)]


    #if j odd
    else:

        #chi(j,k) = z(j-1, k) + sum_{-1,1}(z(j-2, k+i) + x(j-1, k+i))
        chi = [(padded_Z_record[j+2][i+1] \
            + padded_Z_record[j+1][i] + padded_X_record[j+1][i] + padded_Z_record[j+1][i+2] + padded_X_record[j+1][i+2]) %2 \
            for i in range(p*N, (p+1)*N)]

        #zeta(j,k) = z(j-2,k) + x(j-1,k)
        zeta = [(padded_Z_record[j+1][i+1] + padded_X_record[j+1][i+1]) %2 for i in range(p*N, (p+1)*N)]


    #f_jp(D) = tensor(X^chi)D tensor(Z^zeta X^chi)
    X = TensorGate(['X' if x==1 else 'I' for x in chi])
    Z = TensorGate(['Z' if z==1 else 'I' for z in zeta])
    targetD = CompositeGate([X, D, Z, X])
    
    return(targetD)


def main():
    with CQCConnection("Alice") as alice:  

        J = 3 #Depth
        N = 2 #Number of qubits
        M = 2 #Number of sub-qubits : Must be a divider of N
        P = int(N/M)
        L = 1 #Number of steps for the protocol2


        #Recording of the zj and xj, i.e. exponents of the Z and X gates applied in the correction step
        X_record = []
        Z_record = []

        # sum of measurement results from Bob
        cumul_meas = [ 0 for i in range(N) ]

        # Send J to Bob
        alice.sendClassical("Bob", J, close_after=True)


        # Definition of the target gates for all j and all p (J rows, P columns), except the first row which must be a tensor(N) gate
        D_gates = [ [TensorGate(['Z', 'I'])],\
                    [TensorGate(['Z', 'I'])],\
                    [TensorGate(['I', 'I'])],\
                    [TensorGate(['I', 'I'])] ]



        #-------#
        # j = 1 #
        #-------#

        # D_1
        D = D_gates[0][0]
        
        
        keyprev = [ 0 for i in range(N) ]
        key = [ randint(0, 1) for i in range(N) ]

        #save Z_1 = tensor(Z^key)
        Z_record.append(key)

        #save X_1 = I
        X_record.append([0 for i in range(N)])

        send_D_Plus(alice, N, D, key, keyprev)


        #------------#
        # j =2,...,J #
        #------------#

        for j in range(2,J+1):

            new_Xline = []
            new_Zline = []

            for p in range(P):

                targetD = compute_target_gate(j-1, p, M, N, X_record, Z_record, D_gates[j-1][p])
                # targetD = D


                #Send flag to Bob when ready
                alice.sendClassical("Bob", 1, close_after=True)


                #Alice engages protocol 2 and saves the teleportation byproducts and her key
                [Xjp, Zjp] = protocol2(alice, M, L, targetD)

                new_Xline.extend(Xjp)
                new_Zline.extend(Zjp)



            X_record.append(new_Xline)
            Z_record.append(new_Zline)


        #Receiving Bob's measurements in the X basis
        measurements = []
        for i in range(N):
            print("alice: receive measurement")
            meas = alice.recvClassical(close_after=True, timout=10)
            print('meas', int.from_bytes(meas, byteorder='big'))
            measurements.append(int.from_bytes(meas, byteorder='big'))
            print("alice: measurement received")


        #Alice computes the output bits
        O = [(measurements[i] + Z_record[-1][i])%2 for i in range(N)]


        # output should correspond to a measurement of
        # H(D_2HD_1)|+> in the standard basis
        # i.e. if D_1 = (Z tensor I), D_2 = (Z tensor I)
        # then the first bit should be the outcome of measuring
        # HZHZ|+> in the std basis, i.e. 0 or 1 each with prob 0.5

        print(O)


main()