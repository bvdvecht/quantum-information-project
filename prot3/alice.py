from random import randint
import time
import copy
from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from gates import PrimitiveGate, CompositeGate, TensorGate, EntangleGate

class CustomGate(PrimitiveGate):
    def applyOn(self, qubits):
        qubits[0].rot_Z(64) # pi/4 rad

    def applyAdjointOn(self, qubits):
        qubits[0].rot_Z(64) # -pi/4 rad


# key and key_prev are Z_l and Z_{l-1} 
def send_D_Plus(alice, m, D, key, key_prev):
    alice.release_all_qubits()
    
    # create |+>^tensor(m)
    qubits = [qubit(alice) for i in range(m)]
    [ qb.H() for qb in qubits ]
    
    D.applyOn(qubits)
    
    # create encryption gates
    Z_prev = TensorGate(['Z' if bool(r) else 'I' for r in key_prev])
    Z = TensorGate(['Z' if bool(r) else 'I' for r in key])

    Z_prev.applyOn(qubits)
    Z.applyOn(qubits)

    
    for qb in qubits:
        print('alice send_D_Plus: send qbit')
        alice.sendQubit(qb, "Bob")
        print('alice send_D_Plus: qbit sent')

def createNextGate(m, D, measurements):
    # create tensor of X's (if meas=1) and I's (if meas=0)
    X = TensorGate(['X' if m else 'I' for m in measurements])
    D_dagger = copy.copy(D)
    D_dagger.adjoint = True

    # construct D_{l+1} = X_lD_lX_lD_dagger_l
    newD = CompositeGate([X, D, X, D_dagger])

    return newD


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





def protocol2(alice, m, l, D):

    cumul_meas = [ 0 for i in range(m) ]

    key = [ 0 for i in range(m) ]

    # protocol 2
    for i in range(l):
        key_prev = key
        # generate new random key
        key = [ randint(0, 1) for j in range(m) ]

        send_D_Plus(alice, m, D, key, key_prev)

        measurements = []
        for j in range(m):
            print("alice: receive measurement")
            meas = alice.recvClassical(close_after=True, timout=10)
            print('meas', int.from_bytes(meas, byteorder='big'))
            measurements.append(int.from_bytes(meas, byteorder='big'))
            print("alice: measurement received")

        # XOR measurements to cumul_meas for step
        cumul_meas = [(cumul_meas[k] + measurements[k])%2 for k in range(m)]

        # sleep since we don't use recvClassical atm which would block
        # time.sleep(5)

        D = createNextGate(m, D, measurements)

    
    '''result = []
    for i in range(m):
        result.append(alice.recvQubit())

    # result = ZXD|psi>

    # undo Z
    print('undoing Z:', key)
    for i in range(m):
        if key[i] == 1: # Z = Z_l = last key
            result[i].Z()

    # undo X
    print('undoing X:', cumul_meas)
    for i in range(m):
        if cumul_meas[i] == 1:
            result[i].X()'''

    return(cumul_meas, key)




def main():
    with CQCConnection("Alice") as alice:  

        J = 2 #Depth
        N = 2 #Number of qubits
        M = 2 #Number of sub-qubits : Must be a divider of N
        P = int(N/M)
        L = 1 #Number of steps for the protocol2


        #Recording of the zj and xj, i.e. exponents of the Z and X gates applied in the correction step
        X_record = []
        Z_record = []

        # sum of measurement results from Bob
        cumul_meas = [ 0 for i in range(N) ]

        # psi = |+>^tensor(m)
        psi = [ qubit(alice) for i in range(N) ]
        [ qb.H() for qb in psi ]

        # send psi to Bob
        for qb in psi:
            print('alice: send psi qubit')
            alice.sendQubit(qb, "Bob")
            print('alice: psi qubit sent')

        # Send J to Bob
        alice.sendClassical("Bob", J, close_after=True)


        # Definition of the target gates for all j and all p (J rows, P columns), except the first row which must be a tensor(N) gate
        D_gates = [[TensorGate(['Z', 'I'])],\
                    [TensorGate(['I', 'I'])],\
                    [TensorGate(['I', 'I'])],\
                    [TensorGate(['I', 'I'])]]



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

        for j in range(1,J):

            new_Xline = []
            new_Zline = []

            for p in range(P):

                targetD = compute_target_gate(j, p, M, N, X_record, Z_record, D_gates[j][p])


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

        print(O)


        '''# undo X
        print('undoing X:', cumul_meas)
        for i in range(m):
            if cumul_meas[i] == 1:
                result[i].X()

        # measure result, should be |->|+>, i.e. 1 0 in H basis
        [qb.H() for qb in result]
        print("Result: ", result[0].measure(), result[1].measure())'''


main()