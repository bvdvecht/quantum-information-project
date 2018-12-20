from random import randint
from bqc.gates import PrimitiveGate, CompositeGate, TensorGate, EntangleGate
from bqc.prot2 import protocol2, send_D_Plus, protocol2_recv, recv_D_Plus

def compute_target_gate(j, p, N, M, X_record, Z_record, D):

    print('X_record:', X_record)
    print('Z_record:', Z_record)

    offset = 2

    padded_X_record = [ [0 for i in range(M)] for j in range(offset) ]
    padded_Z_record = [ [0 for i in range(M)] for j in range(offset) ]

    padded_X_record.extend(X_record)
    padded_Z_record.extend(Z_record)



    #f_j(D) = HZ(j-1)HDZ(j-2)HX(j-1)Z(j-1)H
    H = TensorGate(['H' for i in range(M)])
    Z1 = TensorGate(['Z' if bool(z) else 'I' for z in padded_Z_record[j-1+offset]])
    Z2 = TensorGate(['Z' if bool(z) else 'I' for z in padded_Z_record[j-2+offset]])
    X1 = TensorGate(['X' if bool(x) else 'I' for x in padded_X_record[j-1+offset]])
    targetD = CompositeGate([H,Z1,H,D,Z2,H,X1,Z1,H])

    print('targetD', targetD)
    
    return(targetD)


# set no_encrypt=True to have easier test case (all keys are 0)
def protocol3_v2(alice, J, N, M, P, L, D_gates, no_encrypt=False):
    #Recording of the zj and xj, i.e. exponents of the Z and X gates applied in the correction step
    X_record = []
    Z_record = []

    # sum of measurement results from Bob
    cumul_meas = [ 0 for i in range(N) ]

    # Send J to Bob
    alice.sendClassical("Bob", J, close_after=True)

    #-------#
    # j = 1 #
    #-------#

    # D_1
    D = D_gates[0][0]
    
    keyprev = [ 0 for i in range(N) ]
    if no_encrypt:
        key = [ 0 for i in range(N) ]
    else:
        key = [ randint(0, 1) for i in range(N) ]

    #save Z_1 = tensor(Z^key)
    Z_record.append(key)

    #save X_1 = I
    X_record.append([0 for i in range(N)])

    print("Alice: sending first gate", D)
    send_D_Plus(alice, N, D, key, keyprev)


    #-------------#
    # j = 2,...,J #
    #-------------#

    for j in range(1, J):

        new_Xline = []
        new_Zline = []

        for p in range(P):

            targetD = compute_target_gate(j, p, M, N, X_record, Z_record, D_gates[j][p])

            #Alice engages protocol 2 and saves the teleportation byproducts and her key
            Xjp, Zjp = protocol2(alice, M, L, targetD, no_encrypt)
            print('prot2 returned:')
            print('\tX:', Xjp)
            print('\tZ:', Zjp)

            new_Xline.extend(Xjp)
            new_Zline.extend(Zjp)



        X_record.append(new_Xline)
        Z_record.append(new_Zline)


    result = []
    #Receiving Bob's measurements in the X basis
    measurements = []
    for i in range(N):
        print("alice: receive measurement")
        meas = alice.recvClassical(close_after=True, timout=10)
        print('meas', int.from_bytes(meas, byteorder='big'))
        measurements.append(int.from_bytes(meas, byteorder='big'))
        print("alice: measurement received")


    #Alice computes the output bits
    print("Z key:", Z_record[-1])
    print("X key:", X_record[-1])
    result = [(measurements[i] + Z_record[-1][i])%2 for i in range(N)]


    '''finalQubits = []
    for i in range(N):
            finalQubits.append(alice.recvQubit())

    #undoing Z
    Zkey = Z_record[-1]
    print("Z Key:", Zkey)
    for i in range(N):
            if Zkey[i] == 1: # Z = Z_l = last key
                    finalQubits[i].Z()

    # undo X
    Xkey = X_record[-1]
    print("X Key:", Xkey)
    for i in range(N):
            if Xkey[i] == 1:
                    finalQubits[i].X()

    finalMeasurement = [qb.measure() for qb in finalQubits]
    print("Final measurement after decryption:", finalMeasurement)'''

    return result


def protocol3_recv_v2(bob, J, N, M, P, L, R):
    #Receives J=1 step qubits
    R = recv_D_Plus(bob, N)

    ###########
    # j=2...J #
    ###########

    for j in range(2, J+1):

        #Bob applies H
        [R[i].H() for i in range(N)]


        for p in range(P):

            #Engage protocol 2
            R = protocol2_recv(bob, M, p, L, R)


        print("Bob depth", j, "done")


    #Bob measures in X basis
    for qb in R:
        qb.H()
        meas = qb.measure()
        #qb.H()
        bob.sendClassical("Alice", meas, close_after=True)


    '''for qb in R:
        print('Bob R: send qbit')
        bob.sendQubit(qb, "Alice")
        print('Bob R: qbit sent')'''
